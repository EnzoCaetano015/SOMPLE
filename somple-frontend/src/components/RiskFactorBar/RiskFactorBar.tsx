import type { CSSProperties } from "react";
import type { RiskFactorBarProps } from "./RiskFactorBar.types";

export const RiskFactorBar = ({ label, value, weight }: RiskFactorBarProps) => {
  const barClass =
    value >= 75 ? "bg-somple-danger" : value >= 40 ? "bg-somple-highlight" : "bg-somple-field";

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm font-medium text-somple-ink">{label}</span>
        <span className="font-mono-num text-[11px] text-somple-muted">
          {value}% · peso {weight}%
        </span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-somple-border">
        <div
          className={`progress-bar h-full rounded-full ${barClass}`}
          style={{ "--progress": `${value}%` } as CSSProperties}
        />
      </div>
    </div>
  );
};
