import json
from typing import Any

from psycopg import Connection


class TelemetryRepository:
    @staticmethod
    def insert_reading(conn: Connection, payload: dict[str, Any]) -> int:
        row = conn.execute(
            """
            INSERT INTO telemetry_readings (
                operation_id, recorded_at, rainfall_mm, temperature_c,
                soil_moisture_pct, soil_type, slope_degrees, distance_to_water_m,
                speed_kmh, latitude, longitude, source
            )
            VALUES (
                %(operation_id)s, %(recorded_at)s, %(rainfall_mm)s, %(temperature_c)s,
                %(soil_moisture_pct)s, %(soil_type)s, %(slope_degrees)s, %(distance_to_water_m)s,
                %(speed_kmh)s, %(latitude)s, %(longitude)s, %(source)s
            )
            RETURNING id
            """,
            payload,
        ).fetchone()
        return int(row["id"])

    @staticmethod
    def get_active_model_version(conn: Connection) -> dict:
        row = conn.execute(
            """
            SELECT id, model_name, version, artifact_sha256
            FROM model_versions
            WHERE is_active = TRUE
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()
        if row is None:
            from utils.errors import ModelUnavailableError

            raise ModelUnavailableError("No active model version configured")
        return row

    @staticmethod
    def insert_assessment(conn: Connection, payload: dict[str, Any]) -> int:
        row = conn.execute(
            """
            INSERT INTO risk_assessments (
                operation_id, telemetry_reading_id, model_version_id,
                risk_score, risk_level, confidence,
                input_snapshot, output_snapshot, explanation_summary
            )
            VALUES (
                %(operation_id)s, %(telemetry_reading_id)s, %(model_version_id)s,
                %(risk_score)s, %(risk_level)s, %(confidence)s,
                %(input_snapshot)s::jsonb, %(output_snapshot)s::jsonb, %(explanation_summary)s
            )
            RETURNING id
            """,
            {
                **payload,
                "input_snapshot": json.dumps(payload["input_snapshot"]),
                "output_snapshot": json.dumps(payload["output_snapshot"]),
            },
        ).fetchone()
        return int(row["id"])

    @staticmethod
    def insert_factor(conn: Connection, assessment_id: int, factor: dict[str, Any]) -> None:
        conn.execute(
            """
            INSERT INTO risk_factors (
                assessment_id, rank, factor_code, factor_label,
                feature_name, feature_value, importance, direction
            )
            VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)
            """,
            (
                assessment_id,
                factor["rank"],
                factor["factor_code"],
                factor["factor_label"],
                factor["feature_name"],
                json.dumps(factor["feature_value"]),
                factor["importance"],
                factor["direction"],
            ),
        )

    @staticmethod
    def insert_alert(conn: Connection, payload: dict[str, Any]) -> int:
        row = conn.execute(
            """
            INSERT INTO alerts (
                assessment_id, severity, status, title, message, recommendation
            )
            VALUES (%(assessment_id)s, %(severity)s, 'open', %(title)s, %(message)s, %(recommendation)s)
            RETURNING id
            """,
            payload,
        ).fetchone()
        return int(row["id"])
