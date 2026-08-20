import { BellOff } from "lucide-react";
import { useAlerts } from "./Alerts.hook";
import { AlertCard } from "@/components/AlertCard/AlertCard";
import { ErrorState } from "@/components/ErrorState/ErrorState";
import { EmptyState } from "@/components/EmptyState/EmptyState";
import { CardsSkeleton } from "@/components/PageSkeleton/PageSkeleton";
import { PageHeader } from "@/components/PageHeader/PageHeader";

export const Alerts = () => {
  const { summary, items, isLoading, isError, isEmpty, refetch, handleOpenAssessment } = useAlerts();

  if (isLoading) return <CardsSkeleton />;
  if (isError) return <ErrorState onRetry={() => void refetch()} />;
  if (!summary || !items) return null;

  return (
    <div className="space-y-6">
      <PageHeader title="Alertas" subtitle={summary} />

      {isEmpty ? (
        <EmptyState
          Icon={BellOff}
          title="Nenhum alerta encontrado."
          description="Não há alertas ativos no momento. A frota está operando dentro dos parâmetros esperados."
        />
      ) : (
        <section className="flex flex-col gap-3">
          {items.map((alert) => (
            <AlertCard
              key={alert.id}
              title={alert.title}
              description={alert.description}
              timeAgo={alert.timeAgo}
              riskLevel={alert.riskLevel}
              actionLabel="Ver detalhes →"
              onAction={() => handleOpenAssessment(alert.assessmentId)}
            />
          ))}
        </section>
      )}
    </div>
  );
};
