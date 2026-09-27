import { Tractor } from "lucide-react";
import { useEquipment } from "./Equipment.hook";
import { EQUIPMENT_COLUMNS } from "./Equipment.utils";
import { EquipmentCard } from "@/components/EquipmentCard/EquipmentCard";
import { ErrorState } from "@/components/ErrorState/ErrorState";
import { EmptyState } from "@/components/EmptyState/EmptyState";
import { FilterBar } from "@/components/FilterBar/FilterBar";
import { CardsSkeleton, TableSkeleton } from "@/components/PageSkeleton/PageSkeleton";
import { PageHeader } from "@/components/PageHeader/PageHeader";
import { SearchInput } from "@/components/SearchInput/SearchInput";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { RiskBadge } from "@/components/RiskBadge/RiskBadge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { NEU_CARD_INSET, NEU_CARD_RAISED } from "@/lib/utils/neumorphic.utils";
import { getScoreTextClass } from "@/lib/utils/risk.utils";
import { cn } from "@/lib/utils";

export const Equipment = () => {
  const {
    totalLabel,
    searchQuery,
    viewMode,
    filters,
    items,
    showSkeleton,
    isError,
    isEmpty,
    refetch,
    handleSearchChange,
    handleViewModeChange,
    handleFilterChange,
    handleSelectEquipment,
  } = useEquipment();

  if (isError) return <ErrorState onRetry={() => void refetch()} />;

  return (
    <div className="space-y-6">
      <PageHeader title="Equipamentos" subtitle={totalLabel} />

      <div className="flex flex-wrap items-center justify-between gap-4">
        <SearchInput
          value={searchQuery}
          onValueChange={handleSearchChange}
          placeholder="Buscar equipamento..."
          className="w-full max-w-md"
        />
        <div className="flex w-full flex-wrap items-center gap-3 sm:w-auto">
          <div className={`${NEU_CARD_INSET} flex flex-1 gap-1 p-1 sm:flex-none`}>
            {(["cards", "table"] as const).map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => handleViewModeChange(mode)}
                className={cn(
                  "flex-1 rounded-[10px] px-4 py-1.5 text-[13px] font-medium transition-all sm:flex-none",
                  viewMode === mode
                    ? `${NEU_CARD_RAISED} text-somple-corporate`
                    : "text-somple-muted hover:text-somple-ink",
                )}
              >
                {mode === "cards" ? "Cards" : "Tabela"}
              </button>
            ))}
          </div>
          <FilterBar filters={filters} onFilterChange={handleFilterChange} />
        </div>
      </div>

      {showSkeleton ? (
        viewMode === "table" ? (
          <TableSkeleton />
        ) : (
          <CardsSkeleton />
        )
      ) : isEmpty ? (
        <EmptyState
          Icon={Tractor}
          title="Nenhum equipamento encontrado."
          description="Nenhum equipamento corresponde à busca ou aos filtros aplicados."
        />
      ) : viewMode === "table" ? (
        <NeumorphicCard className="overflow-hidden p-0">
          <div className="overflow-x-auto" role="region" aria-label="Tabela de equipamentos">
            <Table>
              <TableHeader>
                <TableRow className="border-somple-border/50 hover:bg-transparent">
                  {EQUIPMENT_COLUMNS.map((column) => (
                    <TableHead key={column.key} scope="col" className="text-xs-mono px-4 py-3">
                      {column.label}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {items.map((item) => (
                  <TableRow
                    key={item.id}
                    className="border-somple-border/50 cursor-pointer transition-colors hover:bg-black/3"
                    onClick={() => handleSelectEquipment(item.id)}
                  >
                    <TableCell className="font-mono-num text-sm font-semibold">{item.id}</TableCell>
                    <TableCell className="text-sm">{item.type}</TableCell>
                    <TableCell className="text-sm">{item.region}</TableCell>
                    <TableCell
                      className={`font-mono-num text-right text-base font-bold ${getScoreTextClass(item.riskLevel)}`}
                    >
                      {item.riskScore}
                    </TableCell>
                    <TableCell>
                      <RiskBadge level={item.riskLevel} />
                    </TableCell>
                    <TableCell className="font-mono-num text-[11px] text-somple-muted">
                      {item.lastUpdate}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </NeumorphicCard>
      ) : (
        <section className="grid gap-4.5 sm:grid-cols-1 md:grid-cols-2 xl:grid-cols-3">
          {items.map((item) => (
            <EquipmentCard
              key={item.id}
              id={item.id}
              name={item.name}
              type={item.type}
              riskScore={item.riskScore}
              riskLevel={item.riskLevel}
              lastUpdate={item.lastUpdate}
              onSelect={() => handleSelectEquipment(item.id)}
            />
          ))}
        </section>
      )}
    </div>
  );
};
