import type { Enum } from "@/api/enums/enum";

export type EquipmentDetailViewModel = {
  id: string;
  name: string;
  type: string;
  operation: string;
  region: string;
  score: number;
  riskLevel: Enum.RiskLevel;
  speed: string;
  soilMoisture: string;
  rain: string;
  lastReading: string;
};
