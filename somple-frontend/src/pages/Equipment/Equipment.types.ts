import type { Enum } from "@/api/enums/enum";
import type { FilterDefinition } from "@/components/FilterBar/FilterBar.types";

export type EquipmentItemViewModel = {
  id: string;
  name: string;
  type: string;
  region: string;
  riskScore: number;
  riskLevel: Enum.RiskLevel;
  lastUpdate: string;
};

export type EquipmentViewModel = {
  totalLabel: string;
  searchQuery: string;
  viewMode: "cards" | "table";
  filters: FilterDefinition[];
  items: EquipmentItemViewModel[];
};
