import type { OperationCardProps } from "./OperationCard.types";
import { RiskBadge } from "@/components/RiskBadge/RiskBadge";
import { NEU_CARD_RAISED } from "@/lib/utils/neumorphic.utils";

export const OperationCard = ({
  name,
  area,
  equipmentCount,
  riskLevel,
  status: _status,
}: OperationCardProps) => {
  return (
    <div className={`${NEU_CARD_RAISED} flex items-center justify-between gap-4 p-4`}>
      <div>
        <h3 className="font-semibold text-somple-ink">
          {name} — {area}
        </h3>
        <p className="mt-0.5 text-xs text-somple-muted">{equipmentCount} equipamentos vinculados</p>
      </div>
      <RiskBadge level={riskLevel} />
    </div>
  );
};
