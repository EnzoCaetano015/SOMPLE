from psycopg import Connection


class EquipmentRepository:
    @staticmethod
    def list_equipment(conn: Connection, filters: dict) -> list[dict]:
        clauses = ["1=1"]
        params: list = []
        if filters.get("region_id"):
            clauses.append("region_id = %s")
            params.append(filters["region_id"])
        if filters.get("risk_level"):
            clauses.append("risk_level = %s")
            params.append(filters["risk_level"])
        if filters.get("search"):
            clauses.append("(equipment_code ILIKE %s OR equipment_type ILIKE %s)")
            term = f"%{filters['search']}%"
            params.extend([term, term])
        where = " AND ".join(clauses)
        return conn.execute(
            f"SELECT * FROM v_latest_equipment_state WHERE {where} ORDER BY equipment_code",
            params,
        ).fetchall()

    @staticmethod
    def get_by_code(conn: Connection, equipment_code: str) -> dict | None:
        return conn.execute(
            "SELECT * FROM v_latest_equipment_state WHERE equipment_code = %s LIMIT 1",
            (equipment_code,),
        ).fetchone()
