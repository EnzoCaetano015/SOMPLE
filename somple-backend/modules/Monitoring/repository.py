from psycopg import Connection


class MonitoringRepository:
    @staticmethod
    def fetch_rows(conn: Connection, filters: dict) -> list[dict]:
        clauses = ["1=1"]
        params: list = []
        if filters.get("region_id"):
            clauses.append("region_id = %s")
            params.append(filters["region_id"])
        if filters.get("risk_level"):
            clauses.append("risk_level = %s")
            params.append(filters["risk_level"])
        where = " AND ".join(clauses)
        return conn.execute(
            f"SELECT * FROM v_latest_equipment_state WHERE {where} ORDER BY risk_score DESC NULLS LAST",
            params,
        ).fetchall()
