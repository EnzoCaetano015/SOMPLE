import type { Enum } from "@/api/enums/enum";

export interface OperationCardProps {
  name: string;
  area: string;
  equipmentCount: number;
  riskLevel: Enum.RiskLevel;
  status: Enum.OperationStatus;
}
