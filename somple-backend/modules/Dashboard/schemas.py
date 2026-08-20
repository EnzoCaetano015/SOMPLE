from pydantic import BaseModel


class DashboardSummary(BaseModel):
    monitored_equipment: int
    active_equipment: int
    high_risk_equipment: int
    active_alerts: int
    critical_alerts: int
    average_risk_score: int
    fleet_risk_score: int


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


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    ranking: list[DashboardRankingItem]
    risk_evolution: list[RiskEvolutionPoint]
    risk_distribution: list[RiskDistributionSlice]
    recent_alerts: list[DashboardRecentAlert]
