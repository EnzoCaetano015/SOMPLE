import type { Enum } from "@/api/enums/enum";
import type { FilterDefinition } from "@/components/FilterBar/FilterBar.types";

export type DashboardKpiViewModel = {
  label: string;
  value: string;
  hint: string;
  hintClassName: string;
  iconClassName: string;
  valueClassName?: string;
  variant?: "default" | "alert";
  iconName: "Briefcase" | "AlertTriangle" | "BellRing" | "Activity";
};

export type DashboardRankingItemViewModel = {
  rank: number;
  equipmentId: string;
  equipmentType: string;
  score: number;
  riskLevel: Enum.RiskLevel;
};

export type DashboardAlertViewModel = {
  id: string;
  title: string;
  description: string;
  timeAgo: string;
  assessmentId: string;
  riskLevel: Enum.RiskLevel;
};

export type DashboardChartPoint = {
  label: string;
  value: number;
};

export type DashboardDistributionSlice = {
  name: string;
  value: number;
  color: string;
  dotClass: string;
};

export type DashboardViewModel = {
  kpis: DashboardKpiViewModel[];
  maxRiskScore: number;
  maxRiskLevel: Enum.RiskLevel;
  ranking: DashboardRankingItemViewModel[];
  riskEvolutionData: DashboardChartPoint[];
  riskDistributionData: DashboardDistributionSlice[];
  recentAlerts: DashboardAlertViewModel[];
  filters: FilterDefinition[];
  report: {
    averageRiskScore: number;
    maxRiskScore: number;
    assessmentCount: number;
    alertCount: number;
  };
  trends: Array<{
    key: string;
    label: string;
    averageRiskScore: number;
    maxRiskScore: number;
    assessmentCount: number;
    alertCount: number;
  }>;
};
