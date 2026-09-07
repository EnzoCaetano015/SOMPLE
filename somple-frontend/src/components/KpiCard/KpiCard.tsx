import type { KpiCardProps } from "./KpiCard.types";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { cn } from "@/lib/utils";

export const KpiCard = ({
  label,
  value,
  hint,
  icon: Icon,
  hintClassName,
  iconClassName,
  valueClassName,
  variant = "default",
}: KpiCardProps) => {
  return (
    <NeumorphicCard
      className={cn(
        "relative p-5 pb-6",
        variant === "alert" && "ring-1 ring-inset ring-somple-danger/15",
      )}
    >
      <div
        className={cn(
          "absolute top-5 right-5 flex size-8 items-center justify-center rounded-lg",
          iconClassName ?? "bg-somple-corporate/8 text-somple-corporate",
        )}
      >
        <Icon className="size-4" aria-hidden="true" />
      </div>
      <p className="text-xs font-medium text-somple-muted">{label}</p>
      <p
        className={cn(
          "font-mono-num mt-2 text-[32px] leading-none font-bold tracking-tight",
          valueClassName,
        )}
      >
        {value}
      </p>
      {hint ? (
        <p
          className={cn("font-mono-num mt-1.5 flex items-center gap-1 text-[11px]", hintClassName)}
        >
          {hint}
        </p>
      ) : null}
    </NeumorphicCard>
  );
};
