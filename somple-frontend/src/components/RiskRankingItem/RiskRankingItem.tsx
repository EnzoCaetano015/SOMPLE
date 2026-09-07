import type { RiskRankingItemProps } from "./RiskRankingItem.types";
import { RiskBadge } from "@/components/RiskBadge/RiskBadge";
import { TableCell, TableRow } from "@/components/ui/table";
import { getScoreTextClass } from "@/lib/utils/risk.utils";

export const RiskRankingItem = ({
  rank,
  equipmentId,
  equipmentType,
  score,
  riskLevel,
}: RiskRankingItemProps) => {
  return (
    <TableRow className="border-somple-border/50 transition-colors hover:bg-black/3">
      <TableCell className="font-mono-num w-7 text-[13px] font-bold text-somple-muted">
        {rank}
      </TableCell>
      <TableCell className="font-mono-num text-[13px] font-semibold">{equipmentId}</TableCell>
      <TableCell className="text-sm">{equipmentType}</TableCell>
      <TableCell
        className={`font-mono-num text-right text-base font-bold ${getScoreTextClass(score)}`}
      >
        {score}
      </TableCell>
      <TableCell className="text-right">
        <RiskBadge level={riskLevel} />
      </TableCell>
    </TableRow>
  );
};
