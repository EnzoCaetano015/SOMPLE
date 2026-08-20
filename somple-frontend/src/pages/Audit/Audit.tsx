import { ClipboardList } from "lucide-react";
import { useAudit } from "./Audit.hook";
import { AUDIT_COLUMNS } from "./Audit.utils";
import { ErrorState } from "@/components/ErrorState/ErrorState";
import { EmptyState } from "@/components/EmptyState/EmptyState";
import { FilterBar } from "@/components/FilterBar/FilterBar";
import { TableSkeleton } from "@/components/PageSkeleton/PageSkeleton";
import { PageHeader } from "@/components/PageHeader/PageHeader";
import { RiskBadge } from "@/components/RiskBadge/RiskBadge";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { getScoreTextClass } from "@/lib/utils/risk.utils";

export const Audit = () => {
  const { rows, filters, showSkeleton, isError, isEmpty, refetch, handleFilterChange, handleOpenAssessment } =
    useAudit();

  if (isError) return <ErrorState onRetry={() => void refetch()} />;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Histórico de avaliações"
        subtitle="Consulte avaliações anteriores e trilhas de explicabilidade do modelo."
        actions={<FilterBar filters={filters} onFilterChange={handleFilterChange} />}
      />

      {showSkeleton ? (
        <TableSkeleton />
      ) : isEmpty ? (
        <EmptyState
          Icon={ClipboardList}
          title="Nenhuma avaliação encontrada."
          description="Nenhum registro corresponde ao período ou filtros selecionados."
        />
      ) : (
        <NeumorphicCard className="overflow-hidden p-0">
          <div className="overflow-x-auto" role="region" aria-label="Histórico de avaliações">
            <Table>
              <TableHeader>
                <TableRow className="border-somple-border/50 hover:bg-transparent">
                  {AUDIT_COLUMNS.map((column) => (
                    <TableHead key={column.key} scope="col" className="text-xs-mono px-4 py-3">
                      {column.label}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.map((row) => (
                  <TableRow
                    key={row.id}
                    className="cursor-pointer border-somple-border/50 transition-colors hover:bg-black/3"
                    onClick={() => handleOpenAssessment(row.assessmentId)}
                  >
                    <TableCell className="font-mono-num text-[11px] text-somple-muted">
                      {row.date}
                    </TableCell>
                    <TableCell className="font-mono-num text-sm font-semibold">{row.equipment}</TableCell>
                    <TableCell className="text-sm">{row.operation}</TableCell>
                    <TableCell
                      className={`font-mono-num text-right text-base font-bold ${getScoreTextClass(row.score)}`}
                    >
                      {row.score}
                    </TableCell>
                    <TableCell>
                      <RiskBadge level={row.riskLevel} />
                    </TableCell>
                    <TableCell className="font-mono-num text-[11px]">{row.model}</TableCell>
                    <TableCell className="font-mono-num text-[11px]">{row.version}</TableCell>
                    <TableCell className="text-sm">{row.alert}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </NeumorphicCard>
      )}
    </div>
  );
};
