import type { GetAudit } from "@/api/models/audit.types";
import { formatDateTime } from "@/lib/utils/format.utils";
import type { AuditViewModel } from "./Audit.types";

export const DEFAULT_AUDIT_FILTERS = [
  {
    id: "equipment",
    label: "Equipamento",
    value: "all",
    options: [{ value: "all", label: "Todos" }],
  },
  {
    id: "date",
    label: "Data",
    value: "all",
    options: [
      { value: "all", label: "Todas" },
      { value: "today", label: "Hoje" },
      { value: "week", label: "Semana" },
    ],
  },
  {
    id: "region",
    label: "Região",
    value: "all",
    options: [{ value: "all", label: "Todas" }],
  },
  {
    id: "level",
    label: "Nível",
    value: "all",
    options: [
      { value: "all", label: "Todos" },
      { value: "low", label: "Baixo" },
      { value: "medium", label: "Moderado" },
      { value: "high", label: "Alto" },
      { value: "critical", label: "Crítico" },
    ],
  },
  {
    id: "operation",
    label: "Operação",
    value: "all",
    options: [{ value: "all", label: "Todas" }],
  },
];

export const AUDIT_COLUMNS = [
  { key: "date", label: "Data" },
  { key: "equipment", label: "Equipamento" },
  { key: "operation", label: "Operação" },
  { key: "score", label: "Score" },
  { key: "level", label: "Nível" },
  { key: "model", label: "Modelo" },
  { key: "version", label: "Versão" },
  { key: "alert", label: "Alerta" },
];

export const mapAuditViewModel = (
  data: GetAudit.Response,
  filters = DEFAULT_AUDIT_FILTERS,
): AuditViewModel => ({
  filters,
  rows: data.items.map((row) => ({
    id: String(row.assessment_id),
    assessmentId: String(row.assessment_id),
    date: formatDateTime(row.predicted_at),
    equipment: row.equipment,
    operation: row.operation,
    score: row.score,
    riskLevel: row.risk_level,
    model: row.model_name,
    version: row.model_version,
    alert: row.alert_generated ? "Sim" : "Não",
  })),
});

export const updateAuditFilter = (
  filters: AuditViewModel["filters"],
  filterId: string,
  value: string,
) => filters.map((filter) => (filter.id === filterId ? { ...filter, value } : filter));

export const auditFiltersToParams = (filters: AuditViewModel["filters"]) => {
  const equipment = filters.find((f) => f.id === "equipment")?.value;
  const level = filters.find((f) => f.id === "level")?.value;
  const operation = filters.find((f) => f.id === "operation")?.value;
  const region = filters.find((f) => f.id === "region")?.value;

  return {
    equipment_code: equipment && equipment !== "all" ? equipment : undefined,
    risk_level: level && level !== "all" ? level : undefined,
    operation_type: operation && operation !== "all" ? operation : undefined,
    region_id: region && region !== "all" ? Number(region) : undefined,
  };
};
