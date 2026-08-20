import type { GetOperations } from "@/api/models/operation.types";
import type { OperationsViewModel } from "./Operations.types";

export const mapOperationsViewModel = (data: GetOperations.Response): OperationsViewModel => ({
  items: data.items.map((operation) => ({
    id: operation.key,
    name: operation.name,
    area: operation.region_name,
    equipmentCount: operation.equipment_count,
    riskLevel: operation.risk_level,
    status: operation.status,
  })),
});
