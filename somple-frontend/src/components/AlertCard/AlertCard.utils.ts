import { Enum } from "@/api/enums/enum";

export const ALERT_CARD_VARIANTS: Record<Enum.RiskLevel, string> = {
  [Enum.RiskLevel.LOW]: "bg-somple-bg/50 border border-somple-border/40",
  [Enum.RiskLevel.MEDIUM]: "bg-somple-highlight/8 border border-somple-highlight/15",
  [Enum.RiskLevel.HIGH]: "bg-somple-danger/4 border border-somple-danger/12",
  [Enum.RiskLevel.CRITICAL]: "bg-somple-danger/6 border border-somple-danger/18",
};

export const ALERT_ICON_VARIANTS: Record<Enum.RiskLevel, string> = {
  [Enum.RiskLevel.LOW]: "bg-somple-field/12 text-somple-field",
  [Enum.RiskLevel.MEDIUM]: "bg-somple-highlight/12 text-somple-field",
  [Enum.RiskLevel.HIGH]: "bg-somple-danger/8 text-somple-danger",
  [Enum.RiskLevel.CRITICAL]: "bg-somple-danger/12 text-somple-danger",
};
