from psycopg import Connection

from modules.Dashboard.filters import DashboardFilters


def _where(filters: DashboardFilters, *, include_alerts: bool = False) -> tuple[str, list]:
    clauses = ["ra.predicted_at >= NOW() - %s::interval"]
    params: list = [filters.interval]
    if filters.region_id is not None:
        clauses.append("o.region_id = %s")
        params.append(filters.region_id)
    if filters.operation_category is not None:
        clauses.append("o.operation_category = %s")
        params.append(filters.operation_category)
    if filters.operation_type is not None:
        clauses.append("o.operation_type = %s")
        params.append(filters.operation_type)
    if filters.equipment_id is not None:
        clauses.append("o.equipment_id = %s")
        params.append(filters.equipment_id)
    return " AND ".join(clauses), params


class DashboardRepository:
    @staticmethod
    def fetch_state_rows(conn: Connection, filters: DashboardFilters) -> list[dict]:
        where, params = _where(filters)
        return conn.execute(
            f"""
            SELECT DISTINCT ON (e.id)
                e.id AS equipment_db_id, e.external_code AS equipment_code,
                e.equipment_type, e.status AS equipment_status,
                o.region_id, o.operation_category, o.operation_type,
                ra.risk_score, ra.risk_level, ra.predicted_at
            FROM risk_assessments ra
            JOIN operations o ON o.id = ra.operation_id
            JOIN equipment e ON e.id = o.equipment_id
            WHERE {where}
            ORDER BY e.id, ra.predicted_at DESC, ra.id DESC
            """,
            params,
        ).fetchall()

    @staticmethod
    def fetch_evolution(conn: Connection, filters: DashboardFilters) -> list[dict]:
        where, params = _where(filters)
        bucket = "hour" if filters.period == "24h" else "day"
        return conn.execute(
            f"""
            SELECT date_trunc(%s, ra.predicted_at) AS bucket, AVG(ra.risk_score)::int AS value
            FROM risk_assessments ra
            JOIN operations o ON o.id = ra.operation_id
            WHERE {where}
            GROUP BY bucket
            ORDER BY bucket
            """,
            [bucket, *params],
        ).fetchall()

    @staticmethod
    def fetch_recent_alerts(conn: Connection, filters: DashboardFilters, limit: int = 5) -> list[dict]:
        where, params = _where(filters)
        return conn.execute(
            f"""
            SELECT a.id, a.title, a.message, a.created_at, a.assessment_id, a.severity AS risk_level
            FROM alerts a
            JOIN risk_assessments ra ON ra.id = a.assessment_id
            JOIN operations o ON o.id = ra.operation_id
            WHERE {where}
            ORDER BY a.created_at DESC
            LIMIT %s
            """,
            [*params, limit],
        ).fetchall()

    @staticmethod
    def fetch_report(conn: Connection, filters: DashboardFilters) -> dict:
        where, params = _where(filters)
        return conn.execute(
            f"""
            SELECT
                COALESCE(AVG(ra.risk_score), 0)::int AS average_risk_score,
                COALESCE(MAX(ra.risk_score), 0)::int AS max_risk_score,
                COUNT(DISTINCT ra.id)::int AS assessment_count,
                COUNT(DISTINCT a.id)::int AS alert_count,
                COUNT(DISTINCT a.id) FILTER (WHERE a.status IN ('open', 'acknowledged'))::int AS active_alerts,
                COUNT(DISTINCT a.id) FILTER (
                    WHERE a.status IN ('open', 'acknowledged') AND a.severity = 'critical'
                )::int AS critical_alerts,
                COUNT(DISTINCT ra.id) FILTER (WHERE ra.risk_level = 'low')::int AS low_count,
                COUNT(DISTINCT ra.id) FILTER (WHERE ra.risk_level = 'medium')::int AS medium_count,
                COUNT(DISTINCT ra.id) FILTER (WHERE ra.risk_level = 'high')::int AS high_count,
                COUNT(DISTINCT ra.id) FILTER (WHERE ra.risk_level = 'critical')::int AS critical_count
            FROM risk_assessments ra
            JOIN operations o ON o.id = ra.operation_id
            LEFT JOIN alerts a ON a.assessment_id = ra.id
            WHERE {where}
            """,
            params,
        ).fetchone()

    @staticmethod
    def fetch_trends(conn: Connection, filters: DashboardFilters, dimension: str) -> list[dict]:
        dimensions = {
            "equipment": ("e.id::text", "e.external_code", "JOIN equipment e ON e.id = o.equipment_id"),
            "region": ("r.id::text", "r.name", "JOIN regions r ON r.id = o.region_id"),
            "operation_category": ("o.operation_category", "o.operation_category", ""),
        }
        key, label, join = dimensions[dimension]
        where, params = _where(filters)
        return conn.execute(
            f"""
            SELECT {key} AS key, {label} AS label,
                AVG(ra.risk_score)::int AS average_risk_score,
                MAX(ra.risk_score)::int AS max_risk_score,
                COUNT(DISTINCT ra.id)::int AS assessment_count,
                COUNT(DISTINCT a.id)::int AS alert_count
            FROM risk_assessments ra
            JOIN operations o ON o.id = ra.operation_id
            {join}
            LEFT JOIN alerts a ON a.assessment_id = ra.id
            WHERE {where}
            GROUP BY {key}, {label}
            ORDER BY average_risk_score DESC, label
            """,
            params,
        ).fetchall()

    @staticmethod
    def fetch_filter_options(conn: Connection) -> dict[str, list[dict]]:
        regions = conn.execute("SELECT id::text AS value, name AS label FROM regions ORDER BY name").fetchall()
        categories = conn.execute(
            "SELECT DISTINCT operation_category AS value, operation_category AS label FROM operations ORDER BY 1"
        ).fetchall()
        operation_types = conn.execute(
            "SELECT DISTINCT operation_type AS value, operation_type AS label FROM operations ORDER BY 1"
        ).fetchall()
        return {"regions": regions, "operation_categories": categories, "operation_types": operation_types}
