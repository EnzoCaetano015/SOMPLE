export const API_ROUTES = {
  auth: {
    login: "/auth/login",
    logout: "/auth/logout",
  },
  dashboard: "/dashboard",
  monitoring: "/monitoring",
  equipment: {
    list: "/equipment",
    detail: (code: string) => `/equipment/${code}`,
  },
  operations: "/operations",
  alerts: {
    list: "/alerts",
    status: (id: number | string) => `/alerts/${id}/status`,
  },
  telemetry: {
    create: "/telemetry",
  },
  assessments: {
    detail: (id: number | string) => `/assessments/${id}`,
  },
  audit: {
    history: "/audit",
    events: "/audit/events",
  },
} as const;
