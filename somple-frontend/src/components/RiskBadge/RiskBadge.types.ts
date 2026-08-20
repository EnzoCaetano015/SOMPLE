import { Enum } from "@/api/enums/enum";

export interface RiskBadgeProps {
  level: Enum.RiskLevel;
  className?: string;
}
