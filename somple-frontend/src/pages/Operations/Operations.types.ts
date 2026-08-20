import type { Enum } from "@/api/enums/enum";

export type OperationItemViewModel = {
  id: string;
  name: string;
  area: string;
  equipmentCount: number;
  riskLevel: Enum.RiskLevel;
  status: Enum.OperationStatus;
};

export type OperationsViewModel = {
  items: OperationItemViewModel[];
};
