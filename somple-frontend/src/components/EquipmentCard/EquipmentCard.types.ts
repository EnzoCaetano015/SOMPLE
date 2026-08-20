import type { Enum } from "@/api/enums/enum";

export interface EquipmentCardProps {
  id: string;
  name: string;
  type: string;
  riskScore: number;
  riskLevel: Enum.RiskLevel;
  lastUpdate: string;
  onSelect?: () => void;
}
