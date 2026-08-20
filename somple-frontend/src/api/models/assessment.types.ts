import type { Enum } from "@/api/enums/enum";

export namespace GetAssessment {
  export type Factor = {
    rank: number;
    factor_code: string;
    factor_label: string;
    feature_name: string | null;
    feature_value: unknown;
    importance: number | null;
    direction: string | null;
  };

  export type Response = {
    id: number;
    equipment_id: string;
    equipment_type: string;
    operation: string;
    score: number;
    risk_level: Enum.RiskLevel;
    predicted_at: string;
    model: { name: string; version: string };
    recommendation: string | null;
    factors: Factor[];
    inputs: Record<string, unknown>;
    alert_generated: boolean;
  };
}
