import type { GetAssessment } from "@/api/models/assessment.types";
import { formatDateTime } from "@/lib/utils/format.utils";
import type { AssessmentViewModel } from "./Assessment.types";

const INPUT_LABELS: Record<string, string> = {
  chuva_mm: "Chuva",
  temperatura_c: "Temperatura",
  umidade_solo: "Umidade do solo",
  tipo_solo: "Tipo de solo",
  inclinacao_graus: "Inclinação",
  distancia_agua_m: "Distância da água",
  tipo_operacao: "Operação",
  peso_equipamento_t: "Peso do equipamento",
  dias_desde_manutencao: "Dias desde manutenção",
  incidentes_previos: "Incidentes anteriores",
};

export const mapAssessmentViewModel = (
  assessment: GetAssessment.Response | null | undefined,
): AssessmentViewModel | null => {
  if (!assessment) {
    return null;
  }

  return {
    id: String(assessment.id),
    equipmentId: assessment.equipment_id,
    equipmentName: assessment.equipment_id,
    equipmentType: assessment.equipment_type,
    operation: assessment.operation,
    score: assessment.score,
    riskLevel: assessment.risk_level,
    date: formatDateTime(assessment.predicted_at),
    modelName: assessment.model.name,
    modelVersion: assessment.model.version,
    recommendation: assessment.recommendation ?? "",
    factors: assessment.factors.map((factor) => ({
      label: factor.factor_label,
      value: Number(factor.importance ?? 0) * 100,
      weight: Number(factor.importance ?? 0),
    })),
    inputs: Object.entries(assessment.inputs).map(([key, value]) => ({
      label: INPUT_LABELS[key] ?? key,
      value: String(value),
    })),
    alertGenerated: assessment.alert_generated,
  };
};
