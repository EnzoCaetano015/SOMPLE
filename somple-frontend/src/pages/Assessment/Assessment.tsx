import { FileSearch } from "lucide-react";
import { useAssessment } from "./Assessment.hook";
import { EmptyState } from "@/components/EmptyState/EmptyState";
import { ErrorState } from "@/components/ErrorState/ErrorState";
import { DetailSkeleton } from "@/components/PageSkeleton/PageSkeleton";
import { NeumorphicCard } from "@/components/NeumorphicCard/NeumorphicCard";
import { PageHeader } from "@/components/PageHeader/PageHeader";
import { RiskBadge } from "@/components/RiskBadge/RiskBadge";
import { RiskFactorBar } from "@/components/RiskFactorBar/RiskFactorBar";
import { ScoreGauge } from "@/components/ScoreGauge/ScoreGauge";

export const Assessment = () => {
  const { assessment, isLoading, isError, isEmpty, refetch } = useAssessment();

  if (isLoading) return <DetailSkeleton />;
  if (isError) return <ErrorState onRetry={() => void refetch()} />;
  if (isEmpty || !assessment) {
    return (
      <EmptyState
        Icon={FileSearch}
        title="Avaliação não encontrada"
        description="Não foi possível localizar a avaliação solicitada. Verifique o identificador e tente novamente."
      />
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Avaliação ${assessment.id}`}
        subtitle={`${assessment.equipmentId} · ${assessment.equipmentType}`}
      />

      <section className="grid gap-5.5 xl:grid-cols-[360px_1fr]">
        <ScoreGauge score={assessment.score} label="Score da avaliação" />
        <NeumorphicCard className="grid gap-5 p-6 md:grid-cols-2">
          <div>
            <p className="text-meta">Equipamento</p>
            <p className="mt-1 font-medium text-somple-ink">{assessment.equipmentName}</p>
          </div>
          <div>
            <p className="text-meta">Operação</p>
            <p className="mt-1 font-medium text-somple-ink">{assessment.operation}</p>
          </div>
          <div>
            <p className="text-meta">Data</p>
            <p className="mt-1 font-mono-num font-medium text-somple-ink">{assessment.date}</p>
          </div>
          <div>
            <p className="text-meta">Versão do modelo</p>
            <p className="mt-1 font-mono-num text-sm font-medium text-somple-ink">
              {assessment.modelName} · v{assessment.modelVersion}
            </p>
          </div>
          <div className="md:col-span-2">
            <p className="text-meta">Nível de risco</p>
            <div className="mt-2">
              <RiskBadge level={assessment.riskLevel} />
            </div>
          </div>
        </NeumorphicCard>
      </section>

      <NeumorphicCard className="space-y-5 p-6">
        <h3 className="text-h3 text-somple-ink">Principais fatores</h3>
        {assessment.factors.map((factor) => (
          <RiskFactorBar
            key={factor.label}
            label={factor.label}
            value={factor.value}
            weight={factor.weight}
          />
        ))}
      </NeumorphicCard>

      <NeumorphicCard className="p-6">
        <h3 className="text-h3 text-somple-ink">Recomendação preventiva</h3>
        <p className="mt-3 text-sm leading-6 text-somple-muted">{assessment.recommendation}</p>
      </NeumorphicCard>

      <NeumorphicCard className="p-6">
        <h3 className="text-h3 text-somple-ink">Dados utilizados</h3>
        <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {assessment.inputs.map((input) => (
            <div key={input.label}>
              <p className="text-meta">{input.label}</p>
              <p className="mt-1 font-mono-num font-medium text-somple-ink">{input.value}</p>
            </div>
          ))}
        </div>
      </NeumorphicCard>
    </div>
  );
};
