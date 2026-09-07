import type { GetEquipmentList } from "@/api/models/equipment.types";
import type { FilterDefinition } from "@/components/FilterBar/FilterBar.types";
import { formatTimeAgo } from "@/lib/utils/format.utils";
import { getRiskLevelFromScore } from "@/lib/utils/risk.utils";
import type { EquipmentItemViewModel, EquipmentViewModel } from "./Equipment.types";

export const DEFAULT_EQUIPMENT_FILTERS: FilterDefinition[] = [
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
    id: "risk",
    label: "Risco",
    value: "all",
    options: [
      { value: "all", label: "Todos" },
      { value: "low", label: "Baixo" },
      { value: "medium", label: "Moderado" },
      { value: "high", label: "Alto" },
      { value: "critical", label: "Crítico" },
    ],
  },
];

export const EQUIPMENT_COLUMNS = [
  { key: "id", label: "ID" },
  { key: "type", label: "Tipo" },
  { key: "region", label: "Região" },
  { key: "score", label: "Score" },
  { key: "level", label: "Nível" },
  { key: "lastUpdate", label: "Última leitura" },
] as const;

export const mapEquipmentItems = (data: GetEquipmentList.Response): EquipmentItemViewModel[] =>
  data.items.map((item) => ({
    id: item.equipment_code,
    name: item.equipment_code,
    type: item.equipment_type,
    region: item.region_name ?? "-",
    riskScore: item.risk_score ?? 0,
    riskLevel: item.risk_level ?? getRiskLevelFromScore(item.risk_score ?? 0),
    lastUpdate: formatTimeAgo(item.last_reading_at),
  }));

export const mapEquipmentViewModel = (
  data: GetEquipmentList.Response,
  searchQuery: string,
  viewMode: EquipmentViewModel["viewMode"],
  regionFilter = "all",
  riskFilter = "all",
): EquipmentViewModel => ({
  totalLabel: `${data.total} equipamentos cadastrados`,
  searchQuery,
  viewMode,
  filters: DEFAULT_EQUIPMENT_FILTERS.map((filter) => ({
    ...filter,
    value: filter.id === "region" ? regionFilter : filter.id === "risk" ? riskFilter : filter.value,
  })),
  items: mapEquipmentItems(data),
});

export const equipmentFiltersToParams = (
  searchQuery: string,
  regionFilter: string,
  riskFilter: string,
) => ({
  search: searchQuery.trim() || undefined,
  region_id: regionFilter !== "all" ? Number(regionFilter) : undefined,
  risk_level: riskFilter !== "all" ? riskFilter : undefined,
});
