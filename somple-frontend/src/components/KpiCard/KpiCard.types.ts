import type { LucideIcon } from "lucide-react";

export interface KpiCardProps {
  label: string;
  value: string;
  hint?: string;
  hintClassName?: string;
  iconClassName?: string;
  valueClassName?: string;
  variant?: "default" | "alert";
  icon: LucideIcon;
}
