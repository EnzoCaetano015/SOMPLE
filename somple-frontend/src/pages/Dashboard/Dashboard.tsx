import {
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Activity, AlertTriangle, BellOff, BellRing, ClipboardList } from "lucide-react";

import { useDashboard } from "./Dashboard.hook";
import { KPI_ICON_MAP } from "./Dashboard.utils";
import type { DashboardTrendViewModel } from "./Dashboard.types";
import { Enum } from "@/api/enums/enum";
import { AlertCard } from "@/components/AlertCard/AlertCard";
import { ChartCard } from "@/components/ChartCard/ChartCard";
import { EmptyState } from "@/components/EmptyState/EmptyState";
import { ErrorState } from "@/components/ErrorState/ErrorState";
import { FilterBar } from "@/components/FilterBar/FilterBar";
import { KpiCard } from "@/components/KpiCard/KpiCard";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { DashboardSkeleton } from "@/components/PageSkeleton/PageSkeleton";
import { PageHeader } from "@/components/PageHeader/PageHeader";
import { RiskRankingItem } from "@/components/RiskRankingItem/RiskRankingItem";
import { ScoreGauge } from "@/components/ScoreGauge/ScoreGauge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";
import { formatCount, formatSharePercent } from "@/lib/utils/format.utils";

type TrendTableProps = {
  groupLabel: string;
  ariaLabel: string;
  items: DashboardTrendViewModel[];
};

const TrendTable = ({ groupLabel, ariaLabel, items }: TrendTableProps) => {
  if (items.length === 0) {
    return <div className="p-6 text-sm text-somple-muted">Nenhum dado no recorte selecionado.</div>;
  }

  return (
    <div className="overflow-x-auto" role="region" aria-label={ariaLabel}>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>{groupLabel}</TableHead>
            <TableHead className="text-right">Score médio</TableHead>
            <TableHead className="text-right">Score máximo</TableHead>
            <TableHead className="text-right">Avaliações</TableHead>
            <TableHead className="text-right">Alertas</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {items.map((item) => (
            <TableRow key={item.key}>
              <TableCell>{item.label}</TableCell>
              <TableCell className="text-right font-mono-num">{item.averageRiskScore}</TableCell>
              <TableCell className="text-right font-mono-num">{item.maxRiskScore}</TableCell>
              <TableCell className="text-right font-mono-num">{item.assessmentCount}</TableCell>
              <TableCell className="text-right font-mono-num">{item.alertCount}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export const Dashboard = () => {
  const {
    kpis,
    maxRiskScore,
    maxRiskLevel,
    ranking,
    riskEvolutionData,
    riskDistributionData,
    recentAlerts,
    report,
    trends,
    filters,
    isLoading,
    isError,
    canViewAssessments,
    refetch,
    handleFilterChange,
    handleAlertDetails,
  } = useDashboard();

  if (isLoading) return <DashboardSkeleton />;
  if (isError) return <ErrorState onRetry={() => void refetch()} />;
  if (
    !kpis ||
    !filters ||
    !ranking ||
    !riskEvolutionData ||
    !riskDistributionData ||
    !recentAlerts
  ) {
    return null;
  }

  const distributionTotal = riskDistributionData.reduce((sum, slice) => sum + slice.value, 0);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Visão Geral"
        subtitle="Acompanhe os riscos operacionais e ambientais da sua frota."
        actions={<FilterBar filters={filters} onFilterChange={handleFilterChange} />}
      />

      <section className="grid gap-4.5 sm:grid-cols-1 md:grid-cols-2 xl:grid-cols-4">
        {kpis.map((kpi) => (
          <KpiCard
            key={kpi.label}
            label={kpi.label}
            value={kpi.value}
            hint={kpi.hint}
            hintClassName={kpi.hintClassName}
            iconClassName={kpi.iconClassName}
            valueClassName={kpi.valueClassName}
            variant={kpi.variant}
            icon={KPI_ICON_MAP[kpi.iconName]}
          />
        ))}
      </section>

      <section className="grid gap-5.5 xl:grid-cols-[1fr_1.2fr]">
        <ScoreGauge
          score={maxRiskScore ?? 0}
          riskLevel={maxRiskLevel ?? Enum.RiskLevel.LOW}
          label="Maior score do recorte"
          subtitle="Máximo entre as avaliações filtradas"
        />
        <NeumorphicCard className="overflow-hidden p-0">
          <div className="border-b border-somple-border/50 px-6 py-4">
            <h3 className="text-h3 text-somple-ink">Equipamentos com maior risco</h3>
          </div>
          <div className="overflow-x-auto" role="region" aria-label="Ranking de equipamentos">
            <Table>
              <TableHeader>
                <TableRow className="border-somple-border/50 hover:bg-transparent">
                  <TableHead scope="col" className="text-xs-mono w-7 px-4 py-3">
                    #
                  </TableHead>
                  <TableHead scope="col" className="text-xs-mono px-4 py-3">
                    ID
                  </TableHead>
                  <TableHead scope="col" className="text-xs-mono px-4 py-3">
                    Equipamento
                  </TableHead>
                  <TableHead scope="col" className="text-xs-mono px-4 py-3 text-right">
                    Score
                  </TableHead>
                  <TableHead scope="col" className="text-xs-mono px-4 py-3 text-right">
                    Nível
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {ranking.map((item) => (
                  <RiskRankingItem key={item.equipmentId} {...item} />
                ))}
              </TableBody>
            </Table>
          </div>
        </NeumorphicCard>
      </section>

      <section className="space-y-4" aria-labelledby="consolidated-report-title">
        <div>
          <h3 id="consolidated-report-title" className="text-h3 text-somple-ink">
            Relatório consolidado
          </h3>
          <p className="text-meta mt-1">
            Indicadores calculados com os mesmos filtros da visão geral.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <KpiCard
            icon={Activity}
            label="Score médio"
            value={String(report?.averageRiskScore ?? 0)}
            hint="Média simples"
          />
          <KpiCard
            icon={AlertTriangle}
            label="Score máximo"
            value={String(report?.maxRiskScore ?? 0)}
            hint="Maior avaliação"
          />
          <KpiCard
            icon={ClipboardList}
            label="Avaliações"
            value={String(report?.assessmentCount ?? 0)}
            hint="No período"
          />
          <KpiCard
            icon={BellRing}
            label="Alertas"
            value={String(report?.alertCount ?? 0)}
            hint="Gerados no período"
          />
        </div>
        <NeumorphicCard className="overflow-hidden p-0">
          <div className="border-b border-somple-border/50 px-6 py-4">
            <h4 className="font-semibold text-somple-ink">Comparativos do recorte</h4>
            <p className="text-meta mt-1">Tendências calculadas com os filtros selecionados.</p>
          </div>
          <Tabs defaultValue="equipment" className="gap-0">
            <div className="overflow-x-auto px-4 pt-4 sm:px-6">
              <TabsList aria-label="Agrupamento das tendências" className="min-w-max">
                <TabsTrigger value="equipment" className="min-w-32">
                  Por equipamento
                </TabsTrigger>
                <TabsTrigger value="region" className="min-w-32">
                  Por região
                </TabsTrigger>
                <TabsTrigger value="operation" className="min-w-32">
                  Por operação
                </TabsTrigger>
              </TabsList>
            </div>
            <TabsContent value="equipment">
              <TrendTable
                groupLabel="Equipamento"
                ariaLabel="Tendências por equipamento"
                items={trends?.byEquipment ?? []}
              />
            </TabsContent>
            <TabsContent value="region">
              <TrendTable
                groupLabel="Região"
                ariaLabel="Tendências por região"
                items={trends?.byRegion ?? []}
              />
            </TabsContent>
            <TabsContent value="operation">
              <TrendTable
                groupLabel="Operação"
                ariaLabel="Tendências por categoria de operação"
                items={trends?.byOperationCategory ?? []}
              />
            </TabsContent>
          </Tabs>
        </NeumorphicCard>
      </section>

      <section className="grid gap-5.5 xl:grid-cols-2">
        <ChartCard title="Evolução do risco" subtitle="Score médio no período selecionado">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={riskEvolutionData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#D0D0D0" />
              <XAxis dataKey="label" tick={{ fontSize: 11, fill: "#6B6B6B" }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: "#6B6B6B" }} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#0A4D2E"
                strokeWidth={3}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Distribuição de risco" subtitle="Equipamentos por nível de risco">
          <div className="flex h-full flex-col items-center gap-6 xl:flex-row">
            <div className="min-h-55 w-full flex-1">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={riskDistributionData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius="55%"
                    outerRadius="85%"
                  >
                    {riskDistributionData.map((entry) => (
                      <Cell key={entry.name} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex w-full shrink-0 flex-col gap-3 xl:w-auto">
              {riskDistributionData.map((slice) => (
                <div key={slice.name} className="flex items-center gap-2.5">
                  <span className={cn("size-2.5 shrink-0 rounded-full", slice.dotClass)} />
                  <span className="text-sm text-somple-ink">{slice.name}</span>
                  <span className="font-mono-num ml-auto text-sm font-bold text-somple-ink">
                    {formatCount(slice.value)}
                  </span>
                  <span className="font-mono-num text-[11px] text-somple-muted">
                    ({formatSharePercent(slice.value, distributionTotal)})
                  </span>
                </div>
              ))}
            </div>
          </div>
        </ChartCard>
      </section>

      <section className="space-y-4">
        <div>
          <h3 className="text-h3 text-somple-ink">Alertas recentes</h3>
          <p className="text-meta mt-1">Principais alertas do período selecionado</p>
        </div>
        {recentAlerts.length > 0 ? (
          <div className="grid gap-3">
            {recentAlerts.map((alert) => (
              <AlertCard
                key={alert.id}
                title={alert.title}
                description={alert.description}
                timeAgo={alert.timeAgo}
                riskLevel={alert.riskLevel}
                actionLabel={canViewAssessments ? "Ver detalhes →" : undefined}
                onAction={
                  canViewAssessments ? () => handleAlertDetails(alert.assessmentId) : undefined
                }
              />
            ))}
          </div>
        ) : (
          <EmptyState
            Icon={BellOff}
            title="Nenhum alerta encontrado."
            description="Não há alertas recentes para exibir. Quando novos eventos forem detectados, eles aparecerão aqui."
          />
        )}
      </section>
    </div>
  );
};
