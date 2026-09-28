export const queryKeys = {
  dashboard: (
    period?: string,
    regionId?: number,
    operationCategory?: string,
    operationType?: string,
  ) => ["dashboard", period, regionId, operationCategory, operationType] as const,
  dashboardFilterOptions: ["dashboard", "filter-options"] as const,
  monitoring: (regionId?: number, riskLevel?: string) =>
    ["monitoring", regionId, riskLevel] as const,
  equipment: (search?: string, regionId?: number, riskLevel?: string) =>
    ["equipment", search, regionId, riskLevel] as const,
  equipmentDetail: (id: string) => ["equipment", id] as const,
  alerts: (status?: string, severity?: string) => ["alerts", status, severity] as const,
  operations: ["operations"] as const,
  assessment: (id: string) => ["assessment", id] as const,
  audit: (filters?: Record<string, unknown>) => ["audit", filters] as const,
  auditEvents: (eventType?: string) => ["audit", "events", eventType] as const,
};
