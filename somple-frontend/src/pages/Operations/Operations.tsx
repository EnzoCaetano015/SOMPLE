import { Briefcase } from "lucide-react";
import { useOperations } from "./Operations.hook";
import { ErrorState } from "@/components/ErrorState/ErrorState";
import { EmptyState } from "@/components/EmptyState/EmptyState";
import { OperationCard } from "@/components/OperationCard/OperationCard";
import { CardsSkeleton } from "@/components/PageSkeleton/PageSkeleton";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { PageHeader } from "@/components/PageHeader/PageHeader";

export const Operations = () => {
  const { items, isLoading, isError, isEmpty, refetch } = useOperations();

  if (isLoading) return <CardsSkeleton />;
  if (isError) return <ErrorState onRetry={() => void refetch()} />;
  if (!items) return null;

  return (
    <div className="space-y-6">
      <PageHeader title="Operações" subtitle="Gerencie operações ativas e em andamento" />

      {isEmpty ? (
        <EmptyState
          Icon={Briefcase}
          title="Nenhuma operação encontrada."
          description="Não há operações ativas ou em andamento no momento."
        />
      ) : (
        <NeumorphicCard className="flex flex-col gap-4 p-5">
          {items.map((operation) => (
            <OperationCard
              key={operation.id}
              name={operation.name}
              area={operation.area}
              equipmentCount={operation.equipmentCount}
              riskLevel={operation.riskLevel}
              status={operation.status}
            />
          ))}
        </NeumorphicCard>
      )}
    </div>
  );
};
