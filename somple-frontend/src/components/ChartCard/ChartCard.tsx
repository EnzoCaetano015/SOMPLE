import type { ChartCardProps } from "./ChartCard.types";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";

export const ChartCard = ({ title, subtitle, children }: ChartCardProps) => {
  return (
    <NeumorphicCard className="flex h-full flex-col p-6">
      <div>
        <h3 className="text-h3 text-somple-ink">{title}</h3>
        {subtitle ? <p className="mt-1 text-xs text-somple-muted">{subtitle}</p> : null}
      </div>
      <div className="mt-4 min-h-64 flex-1">{children}</div>
    </NeumorphicCard>
  );
};
