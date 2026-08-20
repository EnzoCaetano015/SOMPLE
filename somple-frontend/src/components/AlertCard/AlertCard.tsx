import { AlertTriangle } from "lucide-react";

import type { AlertCardProps } from "./AlertCard.types";
import { ALERT_CARD_VARIANTS, ALERT_ICON_VARIANTS } from "./AlertCard.utils";
import { cn } from "@/lib/utils";

export const AlertCard = ({
  title,
  description,
  timeAgo,
  actionLabel,
  onAction,
  riskLevel,
}: AlertCardProps) => {
  return (
    <div className={cn("flex gap-3.5 rounded-neumorphic-sm p-4", ALERT_CARD_VARIANTS[riskLevel])}>
      <div
        className={cn(
          "flex size-9 shrink-0 items-center justify-center rounded-[10px]",
          ALERT_ICON_VARIANTS[riskLevel],
        )}
      >
        <AlertTriangle className="size-[18px]" aria-hidden="true" />
      </div>
      <div className="min-w-0 flex-1">
        <h3 className="text-[13px] font-semibold text-somple-ink">{title}</h3>
        <p className="mt-0.5 text-xs leading-snug text-somple-muted">{description}</p>
        <p className="font-mono-num mt-1 text-[10px] text-somple-muted">{timeAgo}</p>
        {actionLabel ? (
          <button
            type="button"
            onClick={onAction}
            className="mt-1.5 text-xs font-semibold text-somple-corporate hover:underline"
          >
            {actionLabel}
          </button>
        ) : null}
      </div>
    </div>
  );
};
