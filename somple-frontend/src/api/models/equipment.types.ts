import type { Enum } from "@/api/enums/enum";

export namespace GetEquipmentList {
  export type Item = {
    equipment_code: string;
    equipment_type: string;
    region_name: string | null;
    equipment_status: Enum.EquipmentStatus;
    risk_score: number | null;
    risk_level: Enum.RiskLevel | null;
    last_reading_at: string | null;
  };

  export type Response = {
    items: Item[];
    total: number;
  };

  export type Params = {
    search?: string;
    region_id?: number;
    risk_level?: string;
  };
}

export namespace GetEquipmentDetail {
  export type Response = {
    equipment: {
      code: string;
      type: string;
      status: Enum.EquipmentStatus;
    };
    current_operation: {
      id: number;
      type: string;
      category: string;
      status: Enum.OperationStatus;
    } | null;
    region: { id: number; name: string } | null;
    latest_telemetry: {
      speed_kmh: number | null;
      soil_moisture_pct: number | null;
      rainfall_mm: number | null;
      recorded_at: string | null;
    } | null;
    latest_assessment: {
      id: number;
      risk_score: number;
      risk_level: Enum.RiskLevel;
      confidence: number | null;
      predicted_at: string | null;
      model_version: string | null;
    } | null;
  };
}
