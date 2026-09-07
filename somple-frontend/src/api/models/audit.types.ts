import type { Enum } from "@/api/enums/enum";

export namespace GetAudit {
  export type Item = {
    assessment_id: number;
    predicted_at: string;
    equipment: string;
    operation: string;
    score: number;
    risk_level: Enum.RiskLevel;
    model_name: string;
    model_version: string;
    alert_generated: boolean;
  };

  export type Response = {
    items: Item[];
  };

  export type Params = {
    equipment_code?: string;
    start_date?: string;
    end_date?: string;
    region_id?: number;
    risk_level?: string;
    operation_type?: string;
  };
}

export namespace GetAuditEvents {
  export type Item = {
    id: number;
    created_at: string;
    event_type: string;
    actor: string | null;
    entity_type: string | null;
    entity_id: number | null;
    request_id: string | null;
    endpoint: string | null;
    http_method: string | null;
    status_code: number | null;
    metadata: Record<string, unknown>;
  };

  export type Response = {
    items: Item[];
  };
}
