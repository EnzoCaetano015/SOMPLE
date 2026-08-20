import type { Enum } from "@/api/enums/enum";
import type { FilterDefinition } from "@/components/FilterBar/FilterBar.types";

export type AuditRowViewModel = {
  id: string;
  assessmentId: string;
  date: string;
  equipment: string;
  operation: string;
  score: number;
  riskLevel: Enum.RiskLevel;
  model: string;
  version: string;
  alert: string;
};

export type AuditViewModel = {
  filters: FilterDefinition[];
  rows: AuditRowViewModel[];
};
