import type { CSSProperties } from "react";
import { Tractor } from "lucide-react";

import type { EquipmentCardProps } from "./EquipmentCard.types";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { RiskBadge } from "@/components/RiskBadge/RiskBadge";
import { getRiskPresentation } from "@/lib/utils/risk.utils";

export const EquipmentCard = ({
  id,
  name,
  type,
  riskScore,
  riskLevel,
  lastUpdate,
  onSelect,
}: EquipmentCardProps) => {
  const presentation = getRiskPresentation(riskLevel);

  return (
    <button type="button" onClick={onSelect} className="w-full text-left">
      <NeumorphicCard className="p-5 transition-all duration-150 hover:-translate-y-px hover:shadow-[5px_5px_14px_rgba(28,28,28,0.14),-5px_-5px_14px_rgba(255,255,255,0.9)]">
        <div className="mb-4 flex items-start justify-between gap-3">
          <div className="flex size-10 items-center justify-center rounded-[10px] bg-somple-corporate/8 text-somple-corporate">
            <Tractor className="size-5" aria-hidden="true" />
          </div>
          <RiskBadge level={riskLevel} />
        </div>
        <p className="font-mono-num text-[13px] font-bold text-somple-ink">{id}</p>
        <p className="text-sm text-somple-muted">{name || type}</p>
        <div className="mt-4 flex items-center gap-2.5">
          <div className="h-1.5 flex-1 overflow-hidden rounded-sm bg-somple-border">
            <div
              className={`progress-bar h-full rounded-sm ${presentation.barClass}`}
              style={{ "--progress": `${riskScore}%` } as CSSProperties}
            />
          </div>
          <span
            className={`font-mono-num min-w-7 text-right text-sm font-bold ${presentation.textClass}`}
          >
            {riskScore}
          </span>
        </div>
        <p className="font-mono-num mt-3.5 text-[10px] text-somple-muted">
          Última leitura: {lastUpdate}
        </p>
      </NeumorphicCard>
    </button>
  );
};
