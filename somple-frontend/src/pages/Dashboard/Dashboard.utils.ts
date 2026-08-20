import { Activity, AlertTriangle, BellRing, Briefcase } from "lucide-react";

import type { GetDashboard } from "@/api/models/dashboard.types";
import { Enum } from "@/api/enums/enum";
import { formatTimeAgo } from "@/lib/utils/format.utils";
import { getRiskPresentation } from "@/lib/utils/risk.utils";
import type {
  DashboardChartPoint,
  DashboardDistributionSlice,
  DashboardKpiViewModel,
  DashboardRankingItemViewModel,
  DashboardViewModel,
} from "./Dashboard.types";

export const DEFAULT_DASHBOARD_FILTERS = [
  {
    id: "period",
    label: "Período",
    value: "7d",
    options: [
      { value: "24h", label: "24 horas" },
      { value: "7d", label: "7 dias" },
      { value: "30d", label: "30 dias" },
    ],
  },
  {
    id: "region",
    label: "Região",
    value: "all",
    options: [
      { value: "all", label: "Todas" },
      { value: "1", label: "Talhão Norte" },
      { value: "2", label: "Talhão Leste" },
      { value: "3", label: "Talhão Sul" },
    ],
  },
  {
    id: "operation",
    label: "Operação",
    value: "all",
    options: [
      { value: "all", label: "Todas" },
      { value: "colheita", label: "Colheita" },
      { value: "plantio", label: "Plantio" },
      { value: "pulverizacao", label: "Pulverização" },
    ],
  },
];

const DISTRIBUTION_COLOR_MAP: Record<Enum.RiskLevel, { color: string; dotClass: string }> = {
  [Enum.RiskLevel.LOW]: { color: "#3C7C3E", dotClass: "bg-somple-field" },
  [Enum.RiskLevel.MEDIUM]: { color: "#8CC63F", dotClass: "bg-somple-highlight" },
  [Enum.RiskLevel.HIGH]: { color: "#E63946", dotClass: "bg-somple-danger" },
  [Enum.RiskLevel.CRITICAL]: { color: "#B91C1C", dotClass: "bg-somple-danger" },
};

export const mapDashboardKpis = (summary: GetDashboard.Summary): DashboardKpiViewModel[] => [
  {
    label: "Equipamentos monitorados",
    value: String(summary.monitored_equipment),
    hint: `${summary.active_equipment} ativos`,
    hintClassName: "text-somple-field",
    iconClassName: "bg-somple-field/12 text-somple-field",
    iconName: "Briefcase",
  },
  {
    label: "Em risco elevado",
    value: String(summary.high_risk_equipment),
    hint: "Alto ou crítico",
    hintClassName: "text-somple-danger",
    iconClassName: "bg-somple-danger/10 text-somple-danger",
    variant: "alert",
    iconName: "AlertTriangle",
  },
  {
    label: "Alertas ativos",
    value: String(summary.active_alerts),
    hint: `${summary.critical_alerts} críticos`,
    hintClassName: summary.critical_alerts > 0 ? "text-somple-danger" : "text-somple-field",
    iconClassName: "bg-somple-highlight/15 text-somple-field",
    iconName: "BellRing",
  },
  {
    label: "Score médio da frota",
    value: String(summary.average_risk_score),
    hint: "Média ponderada",
    hintClassName: "text-somple-muted",
    iconClassName: "bg-somple-surface text-somple-ink",
    iconName: "Activity",
  },
];

export const KPI_ICON_MAP = {
  Briefcase,
  AlertTriangle,
  BellRing,
  Activity,
};

export const mapDashboardRanking = (
  ranking: GetDashboard.RankingItem[],
): DashboardRankingItemViewModel[] =>
  ranking.map((item) => ({
    rank: item.rank,
    equipmentId: item.equipment_id,
    equipmentType: item.equipment_type,
    score: item.score,
    riskLevel: item.risk_level,
  }));

export const mapRiskEvolutionData = (
  data: GetDashboard.RiskEvolutionPoint[],
): DashboardChartPoint[] =>
  data.map((point) => ({
    label: formatTimeAgo(point.timestamp),
    value: point.value,
  }));

export const mapRiskDistributionData = (
  data: GetDashboard.RiskDistributionSlice[],
): DashboardDistributionSlice[] =>
  data.map((slice) => ({
    name: getRiskPresentation(slice.risk_level).label,
    value: slice.count,
    color: DISTRIBUTION_COLOR_MAP[slice.risk_level].color,
    dotClass: DISTRIBUTION_COLOR_MAP[slice.risk_level].dotClass,
  }));

export const mapDashboardViewModel = (
  data: GetDashboard.Response,
  filters = DEFAULT_DASHBOARD_FILTERS,
): DashboardViewModel => ({
  kpis: mapDashboardKpis(data.summary),
  fleetScore: data.summary.fleet_risk_score,
  ranking: mapDashboardRanking(data.ranking),
  riskEvolutionData: mapRiskEvolutionData(data.risk_evolution),
  riskDistributionData: mapRiskDistributionData(data.risk_distribution),
  recentAlerts: data.recent_alerts.map((alert) => ({
    id: String(alert.id),
    title: alert.title,
    description: alert.message,
    timeAgo: formatTimeAgo(alert.created_at),
    assessmentId: String(alert.assessment_id),
    riskLevel: alert.risk_level,
  })),
  filters,
});

export const updateDashboardFilter = (
  filters: DashboardViewModel["filters"],
  filterId: string,
  value: string,
) => filters.map((filter) => (filter.id === filterId ? { ...filter, value } : filter));

export const dashboardFiltersToParams = (filters: DashboardViewModel["filters"]) => {
  const period = filters.find((f) => f.id === "period")?.value;
  const region = filters.find((f) => f.id === "region")?.value;
  const operation = filters.find((f) => f.id === "operation")?.value;

  return {
    period: period && period !== "all" ? period : undefined,
    region_id: region && region !== "all" ? Number(region) : undefined,
    operation_type: operation && operation !== "all" ? operation : undefined,
  };
};
