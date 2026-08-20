import { Inbox } from "lucide-react";

import type { EmptyStateProps } from "./EmptyState.types";
import { EMPTY_STATE_DEFAULT_DESCRIPTION } from "./EmptyState.types";
import { NEU_BTN } from "@/lib/utils/neumorphic.utils";

export const EmptyState = ({
  title,
  description = EMPTY_STATE_DEFAULT_DESCRIPTION,
  Icon = Inbox,
  actionLabel,
  onAction,
}: EmptyStateProps) => {
  return (
    <div className="flex flex-col items-center justify-center rounded-neumorphic bg-somple-bg px-6 py-12 text-center shadow-neumorphic-raised">
      <div className="mb-4 flex size-14 items-center justify-center rounded-full bg-somple-corporate/8 text-somple-corporate shadow-neumorphic-soft">
        <Icon className="size-6" aria-hidden="true" />
      </div>
      <h3 className="text-lg font-semibold text-somple-ink">{title}</h3>
      <p className="mt-2 max-w-md text-sm text-somple-muted">{description}</p>
      {actionLabel && onAction ? (
        <button type="button" onClick={onAction} className={`${NEU_BTN} mt-6 px-5 py-2.5`}>
          {actionLabel}
        </button>
      ) : null}
    </div>
  );
};
