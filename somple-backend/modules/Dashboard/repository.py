from psycopg import Connection


class DashboardRepository:
    @staticmethod
    def fetch_state_rows(conn: Connection, filters: dict) -> list[dict]:
        clauses = ["1=1"]
        params: list = []

        if filters.get("region_id"):
            clauses.append("region_id = %s")
            params.append(filters["region_id"])
        if filters.get("operation_type"):
            clauses.append("operation_type = %s")
            params.append(filters["operation_type"])

        where = " AND ".join(clauses)
        return conn.execute(
            f"""
            SELECT *
            FROM v_latest_equipment_state
            WHERE {where}
            """,
            params,
        ).fetchall()

    @staticmethod
    def fetch_evolution(conn: Connection, period: str | None) -> list[dict]:
        interval = "7 days"
        if period == "24h":
            interval = "1 day"
        elif period == "30d":
            interval = "30 days"
        return conn.execute(
            """
            SELECT date_trunc('hour', predicted_at) AS bucket, AVG(risk_score)::int AS value
            FROM risk_assessments
            WHERE predicted_at >= NOW() - %s::interval
            GROUP BY bucket
            ORDER BY bucket
            """,
            (interval,),
        ).fetchall()

    @staticmethod
    def fetch_recent_alerts(conn: Connection, limit: int = 5) -> list[dict]:
        return conn.execute(
            """
            SELECT id, title, message, created_at, assessment_id, severity AS risk_level
            FROM alerts
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,),
        ).fetchall()

    @staticmethod
    def fetch_alert_counts(conn: Connection) -> dict:
        return conn.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE status IN ('open', 'acknowledged')) AS active_alerts,
                COUNT(*) FILTER (WHERE status IN ('open', 'acknowledged') AND severity = 'critical') AS critical_alerts
            FROM alerts
            """
        ).fetchone()
