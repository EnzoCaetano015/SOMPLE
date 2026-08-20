import type { Enum } from "@/api/enums/enum";
import type { FilterDefinition } from "@/components/FilterBar/FilterBar.types";

export type MonitoringSummaryViewModel = {
  total: number;
  active: number;
  attention: number;
  critical: number;
};

export type MonitoringRowViewModel = {
  id: string;
  equipment: string;
  operation: string;
  region: string;
  speed: string;
  moisture: string;
  rain: string;
  score: number;
  riskLevel: Enum.RiskLevel;
  lastReading: string;
};

export type MonitoringViewModel = {
  summary: MonitoringSummaryViewModel;
  filters: FilterDefinition[];
  rows: MonitoringRowViewModel[];
};
