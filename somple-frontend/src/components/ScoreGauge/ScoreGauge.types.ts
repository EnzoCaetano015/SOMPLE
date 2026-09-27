import type { Enum } from "@/api/enums/enum";

export interface ScoreGaugeProps {
  score: number;
  riskLevel: Enum.RiskLevel;
  label: string;
  subtitle?: string;
}
