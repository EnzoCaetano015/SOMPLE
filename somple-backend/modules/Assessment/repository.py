from psycopg import Connection


class AssessmentRepository:
    @staticmethod
    def get_assessment(conn: Connection, assessment_id: int) -> dict | None:
        return conn.execute(
            """
            SELECT
                ra.*,
                e.external_code AS equipment_code,
                e.equipment_type,
                o.operation_type,
                mv.model_name,
                mv.version AS model_version
            FROM risk_assessments ra
            JOIN operations o ON o.id = ra.operation_id
            JOIN equipment e ON e.id = o.equipment_id
            JOIN model_versions mv ON mv.id = ra.model_version_id
            WHERE ra.id = %s
            LIMIT 1
            """,
            (assessment_id,),
        ).fetchone()

    @staticmethod
    def get_factors(conn: Connection, assessment_id: int) -> list[dict]:
        return conn.execute(
            """
            SELECT rank, factor_code, factor_label, feature_name, feature_value, importance, direction
            FROM risk_factors
            WHERE assessment_id = %s
            ORDER BY rank
            """,
            (assessment_id,),
        ).fetchall()

    @staticmethod
    def has_alert(conn: Connection, assessment_id: int) -> bool:
        row = conn.execute(
            "SELECT 1 FROM alerts WHERE assessment_id = %s LIMIT 1",
            (assessment_id,),
        ).fetchone()
        return row is not None
