import type { Enum } from "@/api/enums/enum";

export type AlertItemViewModel = {
  id: string;
  title: string;
  description: string;
  timeAgo: string;
  assessmentId: string;
  riskLevel: Enum.RiskLevel;
};

export type AlertsViewModel = {
  summary: string;
  items: AlertItemViewModel[];
};
