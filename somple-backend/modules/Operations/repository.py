from psycopg import Connection


class OperationsRepository:
    @staticmethod
    def fetch_grouped(conn: Connection) -> list[dict]:
        return conn.execute(
            """
            SELECT
                o.operation_type,
                r.id AS region_id,
                r.name AS region_name,
                COUNT(DISTINCT e.id) AS equipment_count,
                COALESCE(AVG(v.risk_score), 0)::int AS average_risk_score,
                MAX(v.risk_level) AS risk_level,
                MODE() WITHIN GROUP (ORDER BY o.status) AS status
            FROM operations o
            JOIN regions r ON r.id = o.region_id
            JOIN equipment e ON e.id = o.equipment_id
            LEFT JOIN v_latest_equipment_state v ON v.equipment_id = e.id
            GROUP BY o.operation_type, r.id, r.name
            ORDER BY average_risk_score DESC
            """
        ).fetchall()
