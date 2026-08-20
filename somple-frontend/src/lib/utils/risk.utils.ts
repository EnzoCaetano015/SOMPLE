import type { LucideIcon } from "lucide-react";
import { AlertTriangle, Shield, ShieldAlert, ShieldCheck } from "lucide-react";

import { Enum } from "@/api/enums/enum";

export type RiskPresentation = {
  label: string;
  shortLabel: string;
  textClass: string;
  bgClass: string;
  barClass: string;
  dotClass: string;
  icon: LucideIcon;
};

export const RISK_LEVEL_MAP: Record<Enum.RiskLevel, RiskPresentation> = {
  [Enum.RiskLevel.LOW]: {
    label: "Baixo",
    shortLabel: "Baixo",
    textClass: "text-somple-field",
    bgClass: "bg-somple-field/12 text-somple-field",
    barClass: "bg-somple-field",
    dotClass: "bg-somple-field",
    icon: ShieldCheck,
  },
  [Enum.RiskLevel.MEDIUM]: {
    label: "Moderado",
    shortLabel: "Moderado",
    textClass: "text-somple-field",
    bgClass: "bg-somple-highlight/15 text-somple-field",
    barClass: "bg-somple-highlight",
    dotClass: "bg-somple-highlight",
    icon: Shield,
  },
  [Enum.RiskLevel.HIGH]: {
    label: "Alto",
    shortLabel: "Alto",
    textClass: "text-somple-danger",
    bgClass: "bg-somple-danger/10 text-somple-danger border border-somple-danger/25",
    barClass: "bg-somple-danger",
    dotClass: "bg-somple-danger",
    icon: ShieldAlert,
  },
  [Enum.RiskLevel.CRITICAL]: {
    label: "Crítico",
    shortLabel: "Crítico",
    textClass: "text-somple-danger",
    bgClass: "bg-somple-danger text-somple-white",
    barClass: "bg-somple-danger",
    dotClass: "bg-somple-white",
    icon: AlertTriangle,
  },
};

export const getRiskPresentation = (level: Enum.RiskLevel): RiskPresentation => {
  return RISK_LEVEL_MAP[level];
};

export const getRiskLevelFromScore = (score: number): Enum.RiskLevel => {
  if (score >= 85) return Enum.RiskLevel.CRITICAL;
  if (score >= 60) return Enum.RiskLevel.HIGH;
  if (score >= 35) return Enum.RiskLevel.MEDIUM;
  return Enum.RiskLevel.LOW;
};

export const getScoreTextClass = (score: number): string => {
  return getRiskPresentation(getRiskLevelFromScore(score)).textClass;
};

export const toProgressPercent = (value: number): string => `${value}%`;
