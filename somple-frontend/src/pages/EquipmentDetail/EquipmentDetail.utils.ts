import type { GetEquipmentDetail } from "@/api/models/equipment.types";
import { formatDateTime, formatPercent, formatRain, formatSpeed } from "@/lib/utils/format.utils";
import { getRiskLevelFromScore } from "@/lib/utils/risk.utils";
import type { EquipmentDetailViewModel } from "./EquipmentDetail.types";

export const mapEquipmentDetailViewModel = (
  equipment: GetEquipmentDetail.Response | null | undefined,
): EquipmentDetailViewModel | null => {
  if (!equipment) {
    return null;
  }

  const score = equipment.latest_assessment?.risk_score ?? 0;
  const riskLevel = equipment.latest_assessment?.risk_level ?? getRiskLevelFromScore(score);

  return {
    id: equipment.equipment.code,
    name: equipment.equipment.code,
    type: equipment.equipment.type,
    operation: equipment.current_operation?.type ?? "—",
    region: equipment.region?.name ?? "—",
    score,
    riskLevel,
    speed: formatSpeed(equipment.latest_telemetry?.speed_kmh),
    soilMoisture: formatPercent(equipment.latest_telemetry?.soil_moisture_pct),
    rain: formatRain(equipment.latest_telemetry?.rainfall_mm),
    lastReading: formatDateTime(equipment.latest_telemetry?.recorded_at),
  };
};
