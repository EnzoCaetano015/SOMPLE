from core.database import Database
from modules.Dashboard.repository import DashboardRepository
from modules.Dashboard.schemas import (
    DashboardRankingItem,
    DashboardRecentAlert,
    DashboardResponse,
    DashboardSummary,
    RiskDistributionSlice,
    RiskEvolutionPoint,
)
from utils.datetime_utils import to_iso8601


class DashboardService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = DashboardRepository()

    def get_dashboard(
        self,
        *,
        period: str | None = None,
        region_id: int | None = None,
        operation_type: str | None = None,
    ) -> DashboardResponse:
        rows = self._repository.fetch_state_rows(
            self._conn,
            {"region_id": region_id, "operation_type": operation_type},
        )
        scores = [row["risk_score"] for row in rows if row.get("risk_score") is not None]
        ranking_rows = sorted(
            [row for row in rows if row.get("risk_score") is not None],
            key=lambda row: row["risk_score"],
            reverse=True,
        )[:10]

        distribution: dict[str, int] = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for row in rows:
            level = row.get("risk_level")
            if level in distribution:
                distribution[level] += 1

        alert_counts = self._repository.fetch_alert_counts(self._conn)
        evolution = self._repository.fetch_evolution(self._conn, period)
        recent = self._repository.fetch_recent_alerts(self._conn)

        return DashboardResponse(
            summary=DashboardSummary(
                monitored_equipment=len(rows),
                active_equipment=len([r for r in rows if r.get("equipment_status") == "active"]),
                high_risk_equipment=len(
                    [r for r in rows if r.get("risk_level") in ("high", "critical")]
                ),
                active_alerts=int(alert_counts["active_alerts"] or 0),
                critical_alerts=int(alert_counts["critical_alerts"] or 0),
                average_risk_score=round(sum(scores) / len(scores)) if scores else 0,
                fleet_risk_score=max(scores) if scores else 0,
            ),
            ranking=[
                DashboardRankingItem(
                    rank=index + 1,
                    equipment_id=row["equipment_code"],
                    equipment_type=row["equipment_type"],
                    score=row["risk_score"],
                    risk_level=row["risk_level"],
                )
                for index, row in enumerate(ranking_rows)
            ],
            risk_evolution=[
                RiskEvolutionPoint(timestamp=to_iso8601(row["bucket"]), value=row["value"])
                for row in evolution
            ],
            risk_distribution=[
                RiskDistributionSlice(risk_level=level, count=count)
                for level, count in distribution.items()
            ],
            recent_alerts=[
                DashboardRecentAlert(
                    id=row["id"],
                    title=row["title"],
                    message=row["message"],
                    created_at=to_iso8601(row["created_at"]),
                    assessment_id=row["assessment_id"],
                    risk_level=row["risk_level"],
                )
                for row in recent
            ],
        )


def get_dashboard(**filters) -> DashboardResponse:
    with Database.session() as conn:
        return DashboardService(conn).get_dashboard(**filters)
