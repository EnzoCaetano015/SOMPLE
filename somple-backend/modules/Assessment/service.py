from core.database import Database
from modules.Assessment.repository import AssessmentRepository
from modules.Assessment.schemas import AssessmentDetailResponse, AssessmentFactor
from utils.datetime_utils import to_iso8601
from utils.errors import ResourceNotFoundError


class AssessmentService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = AssessmentRepository()

    def get_detail(self, assessment_id: int) -> AssessmentDetailResponse:
        row = self._repository.get_assessment(self._conn, assessment_id)
        if row is None:
            raise ResourceNotFoundError("Assessment not found")

        factors = self._repository.get_factors(self._conn, assessment_id)
        return AssessmentDetailResponse(
            id=row["id"],
            equipment_id=row["equipment_code"],
            equipment_type=row["equipment_type"],
            operation=row["operation_type"],
            score=row["risk_score"],
            risk_level=row["risk_level"],
            predicted_at=to_iso8601(row["predicted_at"]),
            model={"name": row["model_name"], "version": row["model_version"]},
            recommendation=row.get("explanation_summary"),
            factors=[
                AssessmentFactor(
                    rank=f["rank"],
                    factor_code=f["factor_code"],
                    factor_label=f["factor_label"],
                    feature_name=f.get("feature_name"),
                    feature_value=f.get("feature_value"),
                    importance=float(f["importance"]) if f.get("importance") is not None else None,
                    direction=f.get("direction"),
                )
                for f in factors
            ],
            inputs=row["input_snapshot"],
            alert_generated=self._repository.has_alert(self._conn, assessment_id),
        )


def get_assessment_detail(assessment_id: int) -> AssessmentDetailResponse:
    with Database.session() as conn:
        return AssessmentService(conn).get_detail(assessment_id)
