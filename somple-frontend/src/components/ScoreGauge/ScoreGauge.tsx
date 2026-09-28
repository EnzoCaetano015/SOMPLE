import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";

import type { ScoreGaugeProps } from "./ScoreGauge.types";
import { buildScoreGaugeData } from "./ScoreGauge.utils";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { getRiskPresentation } from "@/lib/utils/risk.utils";

export const ScoreGauge = ({ score, riskLevel, label, subtitle }: ScoreGaugeProps) => {
  const chartData = buildScoreGaugeData(score, riskLevel);
  const presentation = getRiskPresentation(riskLevel);

  return (
    <NeumorphicCard className="flex h-full flex-col p-6">
      <div>
        <h3 className="text-h3 text-somple-ink">{label}</h3>
        {subtitle ? <p className="mt-1 text-xs text-somple-muted">{subtitle}</p> : null}
      </div>
      <div className="relative mx-auto mt-4 h-56 w-full max-w-xs">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              dataKey="value"
              innerRadius="70%"
              outerRadius="100%"
              startAngle={90}
              endAngle={-270}
              stroke="none"
            >
              {chartData.map((entry) => (
                <Cell key={entry.name} fill={entry.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className={`font-mono-num text-[40px] leading-none font-bold ${presentation.textClass}`}
          >
            {score}
          </span>
          <span className="mt-1.5 text-xs font-semibold tracking-wide uppercase">
            {presentation.label}
          </span>
          {subtitle ? (
            <span className="mt-0.5 text-[11px] text-somple-muted">{subtitle}</span>
          ) : null}
        </div>
      </div>
    </NeumorphicCard>
  );
};
