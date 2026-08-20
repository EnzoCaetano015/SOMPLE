import type { RiskBadgeProps } from "./RiskBadge.types";
import { getRiskPresentation } from "@/lib/utils/risk.utils";
import { cn } from "@/lib/utils";

export const RiskBadge = ({ level, className }: RiskBadgeProps) => {
  const presentation = getRiskPresentation(level);
  const Icon = presentation.icon;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 font-mono text-[11px] font-semibold tracking-wide uppercase",
        presentation.bgClass,
        className,
      )}
    >
      <Icon className="size-3 shrink-0" aria-hidden="true" />
      <span
        className={cn("size-[7px] shrink-0 rounded-full", presentation.dotClass)}
        aria-hidden="true"
      />
      {presentation.shortLabel}
    </span>
  );
};
