import type { Enum } from "@/api/enums/enum";

export namespace GetDashboard {
  export type Summary = {
    monitored_equipment: number;
    active_equipment: number;
    high_risk_equipment: number;
    active_alerts: number;
    critical_alerts: number;
    average_risk_score: number;
    fleet_risk_score: number;
  };

  export type RankingItem = {
    rank: number;
    equipment_id: string;
    equipment_type: string;
    score: number;
    risk_level: Enum.RiskLevel;
  };

  export type RiskEvolutionPoint = {
    timestamp: string;
    value: number;
  };

  export type RiskDistributionSlice = {
    risk_level: Enum.RiskLevel;
    count: number;
  };

  export type RecentAlert = {
    id: number;
    title: string;
    message: string;
    created_at: string;
    assessment_id: number;
    risk_level: Enum.RiskLevel;
  };

  export type Response = {
    summary: Summary;
    ranking: RankingItem[];
    risk_evolution: RiskEvolutionPoint[];
    risk_distribution: RiskDistributionSlice[];
    recent_alerts: RecentAlert[];
  };

  export type Params = {
    period?: string;
    region_id?: number;
    operation_type?: string;
  };
}
