import type { Enum } from "@/api/enums/enum";

const SCORE_COLORS: Record<string, string> = {
  low: "#3C7C3E",
  medium: "#8CC63F",
  high: "#E63946",
  critical: "#E63946",
};

export const buildScoreGaugeData = (score: number, riskLevel: Enum.RiskLevel) => {
  const color = SCORE_COLORS[riskLevel];

  return [
    { name: "score", value: score, color },
    { name: "remaining", value: 100 - score, color: "#E5E5E5" },
  ];
};
