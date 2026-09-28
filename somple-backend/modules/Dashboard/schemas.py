from pydantic import BaseModel


class DashboardSummary(BaseModel):
    monitored_equipment: int
    active_equipment: int
    high_risk_equipment: int
    active_alerts: int
    critical_alerts: int
    average_risk_score: int
    average_risk_level: str
    max_risk_score: int
    max_risk_level: str
    assessment_count: int


class DashboardRankingItem(BaseModel):
    rank: int
    equipment_id: str
    equipment_type: str
    score: int
    risk_level: str


class RiskEvolutionPoint(BaseModel):
    timestamp: str
    value: int


class RiskDistributionSlice(BaseModel):
    risk_level: str
    count: int


class DashboardRecentAlert(BaseModel):
    id: int
    title: str
    message: str
    created_at: str
    assessment_id: int
    risk_level: str


class DashboardTrendItem(BaseModel):
    key: str
    label: str
    average_risk_score: int
    max_risk_score: int
    assessment_count: int
    alert_count: int


class DashboardTrends(BaseModel):
    by_equipment: list[DashboardTrendItem]
    by_region: list[DashboardTrendItem]
    by_operation_category: list[DashboardTrendItem]


class DashboardReport(BaseModel):
    average_risk_score: int
    max_risk_score: int
    assessment_count: int
    alert_count: int
    counts_by_level: dict[str, int]
    evolution: list[RiskEvolutionPoint]


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    ranking: list[DashboardRankingItem]
    risk_evolution: list[RiskEvolutionPoint]
    risk_distribution: list[RiskDistributionSlice]
    recent_alerts: list[DashboardRecentAlert]
    report: DashboardReport
    trends: DashboardTrends


class FilterOption(BaseModel):
    value: str
    label: str


class DashboardFilterOptions(BaseModel):
    regions: list[FilterOption]
    operation_categories: list[FilterOption]
    operation_types: list[FilterOption]
