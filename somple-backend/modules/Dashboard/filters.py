from dataclasses import dataclass


PERIOD_INTERVALS = {"24h": "1 day", "7d": "7 days", "30d": "30 days"}


@dataclass(frozen=True)
class DashboardFilters:
    period: str = "7d"
    region_id: int | None = None
    operation_category: str | None = None
    operation_type: str | None = None
    equipment_id: int | None = None

    @property
    def interval(self) -> str:
        return PERIOD_INTERVALS[self.period]
