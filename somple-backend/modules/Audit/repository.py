from psycopg import Connection


class AuditRepository:
    @staticmethod
    def list_events(conn: Connection, *, event_type: str | None = None) -> list[dict]:
        clauses = ["1=1"]
        params: list = []
        if event_type:
            clauses.append("al.event_type = %s")
            params.append(event_type)
        where = " AND ".join(clauses)
        return conn.execute(
            f"""
            SELECT
                al.id,
                al.created_at,
                al.event_type,
                u.email AS actor,
                al.entity_type,
                al.entity_id,
                al.request_id,
                al.endpoint,
                al.http_method,
                al.status_code,
                al.metadata
            FROM audit_logs al
            LEFT JOIN users u ON u.id = al.actor_user_id
            WHERE {where}
            ORDER BY al.created_at DESC
            LIMIT 200
            """,
            params,
        ).fetchall()

    @staticmethod
    def list_assessments(conn: Connection, filters: dict) -> list[dict]:
        clauses = ["1=1"]
        params: list = []
        if filters.get("equipment_code"):
            clauses.append("e.external_code = %s")
            params.append(filters["equipment_code"])
        if filters.get("region_id"):
            clauses.append("r.id = %s")
            params.append(filters["region_id"])
        if filters.get("risk_level"):
            clauses.append("ra.risk_level = %s")
            params.append(filters["risk_level"])
        if filters.get("operation_type"):
            clauses.append("o.operation_type = %s")
            params.append(filters["operation_type"])
        if filters.get("start_date"):
            clauses.append("ra.predicted_at >= %s")
            params.append(filters["start_date"])
        if filters.get("end_date"):
            clauses.append("ra.predicted_at <= %s")
            params.append(filters["end_date"])
        where = " AND ".join(clauses)
        return conn.execute(
            f"""
            SELECT
                ra.id AS assessment_id,
                ra.predicted_at,
                e.external_code AS equipment,
                o.operation_type AS operation,
                ra.risk_score AS score,
                ra.risk_level,
                mv.model_name,
                mv.version AS model_version,
                EXISTS(SELECT 1 FROM alerts a WHERE a.assessment_id = ra.id) AS alert_generated
            FROM risk_assessments ra
            JOIN operations o ON o.id = ra.operation_id
            JOIN equipment e ON e.id = o.equipment_id
            JOIN regions r ON r.id = o.region_id
            JOIN model_versions mv ON mv.id = ra.model_version_id
            WHERE {where}
            ORDER BY ra.predicted_at DESC
            LIMIT 200
            """,
            params,
        ).fetchall()
