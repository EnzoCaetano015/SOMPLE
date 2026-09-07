import type { GetMonitoring } from "@/api/models/monitoring.types";
import type { FilterDefinition } from "@/components/FilterBar/FilterBar.types";
import { formatDateTime, formatPercent, formatRain, formatSpeed } from "@/lib/utils/format.utils";
import { getRiskLevelFromScore } from "@/lib/utils/risk.utils";
import type { MonitoringViewModel } from "./Monitoring.types";

export const DEFAULT_MONITORING_FILTERS: FilterDefinition[] = [
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
    id: "status",
    label: "Risco",
    value: "all",
    options: [
      { value: "all", label: "Todos" },
      { value: "medium", label: "Moderado" },
      { value: "high", label: "Alto" },
      { value: "critical", label: "Crítico" },
    ],
  },
];

export const MONITORING_COLUMNS = [
  { key: "equipment", label: "Equipamento" },
  { key: "operation", label: "Operação" },
  { key: "region", label: "Região" },
  { key: "speed", label: "Velocidade" },
  { key: "moisture", label: "Umidade solo" },
  { key: "rain", label: "Chuva" },
  { key: "score", label: "Score" },
  { key: "status", label: "Status" },
  { key: "lastReading", label: "Última leitura" },
];

export const mapMonitoringViewModel = (
  data: GetMonitoring.Response,
  regionFilter = "all",
  statusFilter = "all",
): MonitoringViewModel => ({
  summary: data.summary,
  filters: DEFAULT_MONITORING_FILTERS.map((filter) => ({
    ...filter,
    value:
      filter.id === "region" ? regionFilter : filter.id === "status" ? statusFilter : filter.value,
  })),
  rows: data.rows.map((row) => {
    const score = row.score ?? 0;
    const riskLevel = row.risk_level ?? getRiskLevelFromScore(score);
    return {
      id: row.id,
      equipment: row.id,
      operation: row.operation,
      region: row.region,
      speed: formatSpeed(row.speed_kmh),
      moisture: formatPercent(row.soil_moisture_pct),
      rain: formatRain(row.rainfall_mm),
      score,
      riskLevel,
      lastReading: formatDateTime(row.last_reading_at),
    };
  }),
});

export const monitoringFiltersToParams = (regionFilter: string, statusFilter: string) => ({
  region_id: regionFilter !== "all" ? Number(regionFilter) : undefined,
  risk_level: statusFilter !== "all" ? statusFilter : undefined,
});
