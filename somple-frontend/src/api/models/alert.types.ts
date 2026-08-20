import type { Enum } from "@/api/enums/enum";

export namespace GetAlerts {
  export type Item = {
    id: number;
    severity: Enum.RiskLevel;
    status: Enum.AlertStatus;
    title: string;
    message: string;
    recommendation: string | null;
    equipment_code: string | null;
    assessment_id: number;
    created_at: string;
    acknowledged_at: string | null;
    resolved_at: string | null;
  };

  export type Response = {
    items: Item[];
  };

  export type Params = {
    status?: string;
    severity?: string;
    equipment_id?: string;
  };
}

export namespace UpdateAlertStatus {
  export type Request = {
    status: Enum.AlertStatus;
  };

  export type Response = {
    id: number;
    status: Enum.AlertStatus;
    acknowledged_at: string | null;
    resolved_at: string | null;
  };
}
