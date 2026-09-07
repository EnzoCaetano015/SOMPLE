import { ClipboardList, ScrollText } from "lucide-react";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const Audit = () => {
  const {
    rows,
    events,
    filters,
    eventType,
    showSkeleton,
    showEventsSkeleton,
    isError,
    isEventsError,
    isEmpty,
    isEventsEmpty,
    refetch,
    refetchEvents,
    handleFilterChange,
    setEventType,
    handleOpenAssessment,
  } = useAudit();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Auditoria"
        subtitle="Consulte avaliações do modelo e eventos de segurança e operação."
      />

      <Tabs defaultValue="assessments">
        <TabsList aria-label="Seções de auditoria">
          <TabsTrigger value="assessments">Avaliações</TabsTrigger>
          <TabsTrigger value="events">Eventos do sistema</TabsTrigger>
        </TabsList>

        <TabsContent value="assessments" className="space-y-4">
          <FilterBar filters={filters} onFilterChange={handleFilterChange} />
          {isError ? (
            <ErrorState onRetry={() => void refetch()} />
          ) : showSkeleton ? (
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
                        <TableCell className="font-mono-num text-sm font-semibold">
                          {row.equipment}
                        </TableCell>
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
        </TabsContent>

        <TabsContent value="events" className="space-y-4">
          <div className="max-w-xs">
            <Select value={eventType} onValueChange={(value) => setEventType(value ?? "all")}>
              <SelectTrigger aria-label="Filtrar por tipo de evento">
                <SelectValue placeholder="Todos os eventos" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos os eventos</SelectItem>
                <SelectItem value="auth.login.failed">Logins inválidos</SelectItem>
                <SelectItem value="auth.login">Logins válidos</SelectItem>
                <SelectItem value="telemetry.received">Telemetria recebida</SelectItem>
                <SelectItem value="risk_assessment.created">Assessments criados</SelectItem>
                <SelectItem value="alert.created">Alertas criados</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {isEventsError ? (
            <ErrorState onRetry={() => void refetchEvents()} />
          ) : showEventsSkeleton ? (
            <TableSkeleton />
          ) : isEventsEmpty ? (
            <EmptyState
              Icon={ScrollText}
              title="Nenhum evento encontrado."
              description="Nenhum evento corresponde ao filtro selecionado."
            />
          ) : (
            <NeumorphicCard className="overflow-hidden p-0">
              <div className="overflow-x-auto" role="region" aria-label="Eventos de auditoria">
                <Table>
                  <TableHeader>
                    <TableRow className="border-somple-border/50 hover:bg-transparent">
                      <TableHead>Data</TableHead>
                      <TableHead>Evento</TableHead>
                      <TableHead>Ator</TableHead>
                      <TableHead>Requisição</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Metadados</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {events.map((event) => (
                      <TableRow key={event.id} className="border-somple-border/50">
                        <TableCell className="font-mono-num text-[11px] text-somple-muted">
                          {new Date(event.created_at).toLocaleString("pt-BR")}
                        </TableCell>
                        <TableCell className="font-mono-num text-xs font-semibold">
                          {event.event_type}
                        </TableCell>
                        <TableCell className="text-xs">
                          {event.actor ?? "Não autenticado"}
                        </TableCell>
                        <TableCell className="font-mono-num text-[11px]">
                          {[event.http_method, event.endpoint, event.request_id]
                            .filter(Boolean)
                            .join(" · ")}
                        </TableCell>
                        <TableCell className="font-mono-num text-xs">
                          {event.status_code ?? "—"}
                        </TableCell>
                        <TableCell className="max-w-sm font-mono-num text-[11px] break-words">
                          {JSON.stringify(event.metadata)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </NeumorphicCard>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};
