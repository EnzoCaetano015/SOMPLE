import type { Enum } from "@/api/enums/enum";

export namespace GetMonitoring {
  export type Summary = {
    total: number;
    active: number;
    attention: number;
    critical: number;
  };

  export type Row = {
    id: string;
    equipment_type: string;
    operation: string;
    region: string;
    speed_kmh: number | null;
    soil_moisture_pct: number | null;
    rainfall_mm: number | null;
    score: number | null;
    risk_level: Enum.RiskLevel | null;
    last_reading_at: string | null;
  };

  export type Response = {
    summary: Summary;
    rows: Row[];
  };

  export type Params = {
    region_id?: number;
    risk_level?: string;
  };
}
