import type { Enum } from "@/api/enums/enum";

export namespace GetOperations {
  export type Item = {
    key: string;
    name: string;
    region_id: number;
    region_name: string;
    equipment_count: number;
    average_risk_score: number;
    risk_level: Enum.RiskLevel;
    status: Enum.OperationStatus;
  };

  export type Response = {
    items: Item[];
  };
}
