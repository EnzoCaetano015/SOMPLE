from fastapi import Request

from core.authorization import AuthenticatedUser
from core.database import Database
from ml.explainer import Explainer
from ml.feature_builder import FeatureBuilder
from ml.recommendations import build_recommendation
from ml.runtime import get_model_runtime
from modules.Audit.service import AuditService
from modules.Telemetry.repository import TelemetryRepository
from modules.Telemetry.schemas import (
    AlertSummary,
    AssessmentSummary,
    CreateTelemetryRequest,
    CreateTelemetryResponse,
)
from utils.errors import ResourceNotFoundError, ValidationError
from utils.risk import is_high_risk


class TelemetryService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = TelemetryRepository()

    def create(self, payload: CreateTelemetryRequest, request: Request, user: AuthenticatedUser) -> CreateTelemetryResponse:
        operation = self._conn.execute(
            "SELECT id FROM operations WHERE id = %s LIMIT 1",
            (payload.operation_id,),
        ).fetchone()
        if operation is None:
            raise ResourceNotFoundError("Operation not found")

        runtime = get_model_runtime()
        runtime.load()

        reading_id = self._repository.insert_reading(
            self._conn,
            {
                "operation_id": payload.operation_id,
                "recorded_at": payload.recorded_at,
                "rainfall_mm": payload.rainfall_mm,
                "temperature_c": payload.temperature_c,
                "soil_moisture_pct": payload.soil_moisture_pct,
                "soil_type": payload.soil_type,
                "slope_degrees": payload.slope_degrees,
                "distance_to_water_m": payload.distance_to_water_m,
                "speed_kmh": payload.speed_kmh,
                "latitude": payload.latitude,
                "longitude": payload.longitude,
                "source": payload.source,
            },
        )

        features = FeatureBuilder.build(
            self._conn,
            operation_id=payload.operation_id,
            telemetry={
                "rainfall_mm": payload.rainfall_mm,
                "temperature_c": payload.temperature_c,
                "soil_moisture_pct": payload.soil_moisture_pct,
                "soil_type": payload.soil_type,
                "slope_degrees": payload.slope_degrees,
                "distance_to_water_m": payload.distance_to_water_m,
            },
            recorded_at=payload.recorded_at,
        )

        prediction = runtime.predict(features)
        pipeline = runtime._pipeline  # noqa: SLF001
        factors = Explainer.explain(pipeline, features, prediction)
        recommendation = build_recommendation(features, factors)

        model_version = self._repository.get_active_model_version(self._conn)
        assessment_id = self._repository.insert_assessment(
            self._conn,
            {
                "operation_id": payload.operation_id,
                "telemetry_reading_id": reading_id,
                "model_version_id": model_version["id"],
                "risk_score": prediction.risk_score,
                "risk_level": prediction.risk_level,
                "confidence": prediction.confidence,
                "input_snapshot": features.model_dump(),
                "output_snapshot": {
                    "class_probabilities": prediction.class_probabilities,
                    "score_method": prediction.score_method,
                    "explanation_method": factors[0]["explanation_method"] if factors else prediction.explanation_method,
                },
                "explanation_summary": recommendation,
            },
        )

        for factor in factors:
            self._repository.insert_factor(self._conn, assessment_id, factor)

        alert_summary = AlertSummary(generated=False, id=None)
        if is_high_risk(prediction.risk_level):
            alert_id = self._repository.insert_alert(
                self._conn,
                {
                    "assessment_id": assessment_id,
                    "severity": prediction.risk_level,
                    "title": f"Risco {prediction.risk_level} detectado",
                    "message": f"Score {prediction.risk_score} identificado para operação {payload.operation_id}.",
                    "recommendation": recommendation,
                },
            )
            alert_summary = AlertSummary(generated=True, id=alert_id)
            AuditService(self._conn).log_event(
                event_type="alert.created",
                request=request,
                actor_user_id=user.id,
                entity_type="alert",
                entity_id=alert_id,
                status_code=201,
                metadata={"assessment_id": assessment_id},
            )

        audit = AuditService(self._conn)
        audit.log_event(
            event_type="telemetry.received",
            request=request,
            actor_user_id=user.id,
            entity_type="telemetry_reading",
            entity_id=reading_id,
            status_code=201,
            metadata={"operation_id": payload.operation_id},
        )
        audit.log_event(
            event_type="risk_assessment.created",
            request=request,
            actor_user_id=user.id,
            entity_type="risk_assessment",
            entity_id=assessment_id,
            status_code=201,
            metadata={"risk_level": prediction.risk_level, "risk_score": prediction.risk_score},
        )

        return CreateTelemetryResponse(
            telemetry_reading_id=reading_id,
            assessment=AssessmentSummary(
                id=assessment_id,
                risk_score=prediction.risk_score,
                risk_level=prediction.risk_level,
                confidence=prediction.confidence,
                model_version=model_version["version"],
            ),
            alert=alert_summary,
        )

    @staticmethod
    def validate_payload(payload: CreateTelemetryRequest) -> CreateTelemetryRequest:
        if payload.soil_moisture_pct > 100 or payload.soil_moisture_pct < 0:
            raise ValidationError("soil_moisture_pct must be between 0 and 100")
        return payload


def create_telemetry(payload: CreateTelemetryRequest, request: Request, user: AuthenticatedUser) -> CreateTelemetryResponse:
    TelemetryService.validate_payload(payload)
    with Database.transaction() as conn:
        return TelemetryService(conn).create(payload, request, user)
