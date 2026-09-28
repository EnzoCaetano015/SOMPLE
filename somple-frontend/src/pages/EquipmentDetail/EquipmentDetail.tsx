import { Tractor } from "lucide-react";
import { useEquipmentDetail } from "./EquipmentDetail.hook";
import { EmptyState } from "@/components/EmptyState/EmptyState";
import { ErrorState } from "@/components/ErrorState/ErrorState";
import { DetailSkeleton } from "@/components/PageSkeleton/PageSkeleton";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { PageHeader } from "@/components/PageHeader/PageHeader";
import { RiskBadge } from "@/components/RiskBadge/RiskBadge";
import { ScoreGauge } from "@/components/ScoreGauge/ScoreGauge";

export const EquipmentDetail = () => {
  const { equipment, isLoading, isError, isEmpty, refetch } = useEquipmentDetail();

  if (isLoading) return <DetailSkeleton />;
  if (isError) return <ErrorState onRetry={() => void refetch()} />;
  if (isEmpty || !equipment) {
    return (
      <EmptyState
        Icon={Tractor}
        title="Equipamento não encontrado"
        description="Verifique o identificador informado na URL ou retorne à listagem de equipamentos."
      />
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader title={equipment.id} subtitle={`${equipment.name} · ${equipment.type}`} />

      <section className="grid gap-5.5 xl:grid-cols-[360px_1fr]">
        <ScoreGauge
          score={equipment.score}
          riskLevel={equipment.riskLevel}
          label="Score operacional"
        />
        <NeumorphicCard className="grid gap-5 p-6 md:grid-cols-2">
          <div>
            <p className="text-meta">Operação</p>
            <p className="mt-1 font-medium text-somple-ink">{equipment.operation}</p>
          </div>
          <div>
            <p className="text-meta">Região</p>
            <p className="mt-1 font-medium text-somple-ink">{equipment.region}</p>
          </div>
          <div>
            <p className="text-meta">Velocidade</p>
            <p className="mt-1 font-mono-num font-medium text-somple-ink">{equipment.speed}</p>
          </div>
          <div>
            <p className="text-meta">Umidade do solo</p>
            <p className="mt-1 font-mono-num font-medium text-somple-ink">
              {equipment.soilMoisture}
            </p>
          </div>
          <div>
            <p className="text-meta">Chuva</p>
            <p className="mt-1 font-mono-num font-medium text-somple-ink">{equipment.rain}</p>
          </div>
          <div>
            <p className="text-meta">Última leitura</p>
            <p className="mt-1 font-mono-num text-sm font-medium text-somple-ink">
              {equipment.lastReading}
            </p>
          </div>
          <div className="md:col-span-2">
            <p className="text-meta">Nível de risco</p>
            <div className="mt-2">
              <RiskBadge level={equipment.riskLevel} />
            </div>
          </div>
        </NeumorphicCard>
      </section>
    </div>
  );
};
