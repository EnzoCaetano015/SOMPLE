import type { Enum } from "@/api/enums/enum";

export interface RiskRankingItemProps {
  rank: number;
  equipmentId: string;
  equipmentType: string;
  score: number;
  riskLevel: Enum.RiskLevel;
}
