import type { Enum } from "@/api/enums/enum";

export type AssessmentFactorViewModel = {
  label: string;
  value: number;
  weight: number;
};

export type AssessmentInputViewModel = {
  label: string;
  value: string;
};

export type AssessmentViewModel = {
  id: string;
  equipmentId: string;
  equipmentName: string;
  equipmentType: string;
  operation: string;
  score: number;
  riskLevel: Enum.RiskLevel;
  date: string;
  modelName: string;
  modelVersion: string;
  recommendation: string;
  factors: AssessmentFactorViewModel[];
  inputs: AssessmentInputViewModel[];
  alertGenerated: boolean;
};
