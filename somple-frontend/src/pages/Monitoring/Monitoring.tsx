import { Activity } from "lucide-react";

import { useMonitoring } from "./Monitoring.hook";

import { MONITORING_COLUMNS } from "./Monitoring.utils";

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



export const Monitoring = () => {

  const { summary, filters, rows, showSkeleton, isError, isEmpty, refetch, handleFilterChange } =

    useMonitoring();



  if (isError) return <ErrorState onRetry={() => void refetch()} />;



  return (

    <div className="space-y-6">

      <PageHeader

        title="Monitoramento operacional"

        subtitle="Dados de telemetria em tempo quase real da sua frota."

        actions={<FilterBar filters={filters} onFilterChange={handleFilterChange} />}

      />



      {showSkeleton ? (

        <TableSkeleton />

      ) : isEmpty ? (

        <EmptyState

          Icon={Activity}

          title="Nenhum equipamento encontrado."

          description="Nenhum equipamento corresponde à região ou ao nível de risco selecionados."

        />

      ) : (

        <>

          <div className="flex flex-wrap gap-6 md:gap-8">

            <div>

              <p className="font-mono-num text-[28px] leading-none font-bold text-somple-ink">

                {summary?.total}

              </p>

              <p className="text-meta mt-1">equipamentos</p>

            </div>

            <div>

              <p className="font-mono-num text-[28px] leading-none font-bold text-somple-field">

                {summary?.active}

              </p>

              <p className="text-meta mt-1">ativos</p>

            </div>

            <div>

              <p className="font-mono-num text-[28px] leading-none font-bold text-somple-highlight">

                {summary?.attention}

              </p>

              <p className="text-meta mt-1">em atenção</p>

            </div>

            <div>

              <p className="font-mono-num text-[28px] leading-none font-bold text-somple-danger">

                {summary?.critical}

              </p>

              <p className="text-meta mt-1">críticos</p>

            </div>

          </div>



          <NeumorphicCard className="overflow-hidden p-0">

            <div className="flex items-center justify-end border-b border-somple-border/50 px-6 py-3">

              <span className="mr-2 size-2 animate-somple-pulse rounded-full bg-somple-highlight" />

              <span className="font-mono-num text-[11px] text-somple-field">Monitoramento ativo</span>

            </div>

            <div className="overflow-x-auto" role="region" aria-label="Tabela de monitoramento">

              <Table>

                <TableHeader>

                  <TableRow className="border-somple-border/50 hover:bg-transparent">

                    {MONITORING_COLUMNS.map((column) => (

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

                      className="border-somple-border/50 transition-colors hover:bg-black/3"

                    >

                      <TableCell className="text-sm">{row.equipment}</TableCell>

                      <TableCell className="text-sm">{row.operation}</TableCell>

                      <TableCell className="text-sm">{row.region}</TableCell>

                      <TableCell className="font-mono-num text-sm">{row.speed}</TableCell>

                      <TableCell className="font-mono-num text-sm">{row.moisture}</TableCell>

                      <TableCell className="font-mono-num text-sm">{row.rain}</TableCell>

                      <TableCell

                        className={`font-mono-num text-right text-base font-bold ${getScoreTextClass(row.score)}`}

                      >

                        {row.score}

                      </TableCell>

                      <TableCell>

                        <RiskBadge level={row.riskLevel} />

                      </TableCell>

                      <TableCell className="font-mono-num text-[10px] text-somple-muted">

                        {row.lastReading}

                      </TableCell>

                    </TableRow>

                  ))}

                </TableBody>

              </Table>

            </div>

          </NeumorphicCard>

        </>

      )}

    </div>

  );

};

