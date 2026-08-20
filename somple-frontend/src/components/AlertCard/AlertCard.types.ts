import type { Enum } from "@/api/enums/enum";

export interface AlertCardProps {
  title: string;
  description: string;
  timeAgo: string;
  actionLabel?: string;
  onAction?: () => void;
  riskLevel: Enum.RiskLevel;
}
