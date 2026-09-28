from core.database import Database
from modules.Dashboard.filters import DashboardFilters
from modules.Dashboard.repository import DashboardRepository
from modules.Dashboard.schemas import (
    DashboardFilterOptions, DashboardRankingItem, DashboardRecentAlert,
    DashboardReport, DashboardResponse, DashboardSummary, DashboardTrendItem,
    DashboardTrends, FilterOption, RiskDistributionSlice, RiskEvolutionPoint,
)
from utils.datetime_utils import to_iso8601
from utils.risk import risk_level_from_score

CATEGORY_LABELS = {"field": "Campo", "transport": "Transporte", "near_water": "Próximo à água"}


class DashboardService:
    def __init__(self, conn):
        self._conn = conn
        self._repository = DashboardRepository()

    def get_dashboard(self, filters: DashboardFilters) -> DashboardResponse:
        rows = self._repository.fetch_state_rows(self._conn, filters)
        ranking_rows = sorted(rows, key=lambda row: row["risk_score"], reverse=True)[:10]
        distribution = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for row in rows:
            distribution[row["risk_level"]] += 1

        report = self._repository.fetch_report(self._conn, filters)
        evolution = [
            RiskEvolutionPoint(timestamp=to_iso8601(row["bucket"]), value=row["value"])
            for row in self._repository.fetch_evolution(self._conn, filters)
        ]
        counts_by_level = {
            level: int(report[f"{level}_count"] or 0)
            for level in ("low", "medium", "high", "critical")
        }

        def trend_items(dimension: str) -> list[DashboardTrendItem]:
            result = []
            for row in self._repository.fetch_trends(self._conn, filters, dimension):
                label = CATEGORY_LABELS.get(row["label"], str(row["label"]))
                result.append(DashboardTrendItem(
                    key=str(row["key"]), label=label,
                    average_risk_score=int(row["average_risk_score"] or 0),
                    max_risk_score=int(row["max_risk_score"] or 0),
                    assessment_count=int(row["assessment_count"] or 0),
                    alert_count=int(row["alert_count"] or 0),
                ))
            return result

        return DashboardResponse(
            summary=DashboardSummary(
                monitored_equipment=len(rows),
                active_equipment=sum(row["equipment_status"] == "active" for row in rows),
                high_risk_equipment=sum(row["risk_level"] in {"high", "critical"} for row in rows),
                active_alerts=int(report["active_alerts"] or 0),
                critical_alerts=int(report["critical_alerts"] or 0),
                average_risk_score=int(report["average_risk_score"] or 0),
                average_risk_level=risk_level_from_score(int(report["average_risk_score"] or 0)),
                max_risk_score=int(report["max_risk_score"] or 0),
                max_risk_level=risk_level_from_score(int(report["max_risk_score"] or 0)),
                assessment_count=int(report["assessment_count"] or 0),
            ),
            ranking=[DashboardRankingItem(
                rank=index + 1, equipment_id=row["equipment_code"],
                equipment_type=row["equipment_type"], score=row["risk_score"],
                risk_level=row["risk_level"],
            ) for index, row in enumerate(ranking_rows)],
            risk_evolution=evolution,
            risk_distribution=[
                RiskDistributionSlice(risk_level=level, count=count)
                for level, count in distribution.items()
            ],
            recent_alerts=[DashboardRecentAlert(
                id=row["id"], title=row["title"], message=row["message"],
                created_at=to_iso8601(row["created_at"]), assessment_id=row["assessment_id"],
                risk_level=row["risk_level"],
            ) for row in self._repository.fetch_recent_alerts(self._conn, filters)],
            report=DashboardReport(
                average_risk_score=int(report["average_risk_score"] or 0),
                max_risk_score=int(report["max_risk_score"] or 0),
                assessment_count=int(report["assessment_count"] or 0),
                alert_count=int(report["alert_count"] or 0),
                counts_by_level=counts_by_level,
                evolution=evolution,
            ),
            trends=DashboardTrends(
                by_equipment=trend_items("equipment"),
                by_region=trend_items("region"),
                by_operation_category=trend_items("operation_category"),
            ),
        )

    def get_filter_options(self) -> DashboardFilterOptions:
        options = self._repository.fetch_filter_options(self._conn)
        return DashboardFilterOptions(
            regions=[FilterOption(**row) for row in options["regions"]],
            operation_categories=[FilterOption(
                value=row["value"], label=CATEGORY_LABELS.get(row["value"], row["label"])
            ) for row in options["operation_categories"]],
            operation_types=[FilterOption(value=row["value"], label=row["label"].capitalize())
                             for row in options["operation_types"]],
        )


def get_dashboard(**filters) -> DashboardResponse:
    with Database.session() as conn:
        return DashboardService(conn).get_dashboard(DashboardFilters(**filters))


def get_dashboard_filter_options() -> DashboardFilterOptions:
    with Database.session() as conn:
        return DashboardService(conn).get_filter_options()
