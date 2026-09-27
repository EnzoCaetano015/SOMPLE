import type { Enum } from "@/api/enums/enum";

export namespace GetDashboard {
  export type Summary = {
    monitored_equipment: number;
    active_equipment: number;
    high_risk_equipment: number;
    active_alerts: number;
    critical_alerts: number;
    average_risk_score: number;
    average_risk_level: Enum.RiskLevel;
    max_risk_score: number;
    max_risk_level: Enum.RiskLevel;
    assessment_count: number;
  };
  export type RankingItem = {
    rank: number;
    equipment_id: string;
    equipment_type: string;
    score: number;
    risk_level: Enum.RiskLevel;
  };
  export type RiskEvolutionPoint = { timestamp: string; value: number };
  export type RiskDistributionSlice = { risk_level: Enum.RiskLevel; count: number };
  export type RecentAlert = {
    id: number;
    title: string;
    message: string;
    created_at: string;
    assessment_id: number;
    risk_level: Enum.RiskLevel;
  };
  export type TrendItem = {
    key: string;
    label: string;
    average_risk_score: number;
    max_risk_score: number;
    assessment_count: number;
    alert_count: number;
  };
  export type Report = {
    average_risk_score: number;
    max_risk_score: number;
    assessment_count: number;
    alert_count: number;
    counts_by_level: Record<Enum.RiskLevel, number>;
    evolution: RiskEvolutionPoint[];
  };
  export type Response = {
    summary: Summary;
    ranking: RankingItem[];
    risk_evolution: RiskEvolutionPoint[];
    risk_distribution: RiskDistributionSlice[];
    recent_alerts: RecentAlert[];
    report: Report;
    trends: {
      by_equipment: TrendItem[];
      by_region: TrendItem[];
      by_operation_category: TrendItem[];
    };
  };
  export type Params = {
    period?: "24h" | "7d" | "30d";
    region_id?: number;
    operation_category?: "field" | "transport" | "near_water";
    operation_type?: string;
  };
}

export namespace GetDashboardFilterOptions {
  export type Option = { value: string; label: string };
  export type Response = {
    regions: Option[];
    operation_categories: Option[];
    operation_types: Option[];
  };
}
