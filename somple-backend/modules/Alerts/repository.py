from psycopg import Connection


class AlertsRepository:
    @staticmethod
    def list_alerts(conn: Connection, filters: dict) -> list[dict]:
        clauses = ["1=1"]
        params: list = []
        if filters.get("status"):
            clauses.append("a.status = %s")
            params.append(filters["status"])
        if filters.get("severity"):
            clauses.append("a.severity = %s")
            params.append(filters["severity"])
        if filters.get("equipment_id"):
            clauses.append("e.external_code = %s")
            params.append(filters["equipment_id"])
        where = " AND ".join(clauses)
        return conn.execute(
            f"""
            SELECT
                a.id, a.severity, a.status, a.title, a.message, a.recommendation,
                a.created_at, a.acknowledged_at, a.resolved_at,
                a.assessment_id, e.external_code AS equipment_code
            FROM alerts a
            JOIN risk_assessments ra ON ra.id = a.assessment_id
            JOIN operations o ON o.id = ra.operation_id
            JOIN equipment e ON e.id = o.equipment_id
            WHERE {where}
            ORDER BY a.created_at DESC
            """,
            params,
        ).fetchall()

    @staticmethod
    def get_alert(conn: Connection, alert_id: int) -> dict | None:
        return conn.execute(
            "SELECT * FROM alerts WHERE id = %s LIMIT 1",
            (alert_id,),
        ).fetchone()

    @staticmethod
    def update_status(conn: Connection, alert_id: int, payload: dict) -> dict:
        return conn.execute(
            """
            UPDATE alerts
            SET
                status = %(status)s,
                acknowledged_by = COALESCE(%(acknowledged_by)s, acknowledged_by),
                acknowledged_at = COALESCE(%(acknowledged_at)s, acknowledged_at),
                resolved_at = COALESCE(%(resolved_at)s, resolved_at)
            WHERE id = %(alert_id)s
            RETURNING id, status, acknowledged_at, resolved_at
            """,
            {"alert_id": alert_id, **payload},
        ).fetchone()
