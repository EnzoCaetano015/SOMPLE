import { getRiskLevelFromScore } from "@/lib/utils/risk.utils";

const SCORE_COLORS: Record<string, string> = {
  low: "#3C7C3E",
  medium: "#8CC63F",
  high: "#E63946",
  critical: "#E63946",
};

export const buildScoreGaugeData = (score: number) => {
  const level = getRiskLevelFromScore(score);
  const color = SCORE_COLORS[level];

  return [
    { name: "score", value: score, color },
    { name: "remaining", value: 100 - score, color: "#E5E5E5" },
  ];
};
