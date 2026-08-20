import type { GetAlerts } from "@/api/models/alert.types";
import { Enum } from "@/api/enums/enum";
import { formatTimeAgo } from "@/lib/utils/format.utils";
import type { AlertsViewModel } from "./Alerts.types";

export const mapAlertsViewModel = (data: GetAlerts.Response): AlertsViewModel => {
  const critical = data.items.filter((item) => item.severity === Enum.RiskLevel.CRITICAL).length;
  const high = data.items.filter((item) => item.severity === Enum.RiskLevel.HIGH).length;
  const moderate = data.items.filter((item) => item.severity === Enum.RiskLevel.MEDIUM).length;

  return {
    summary: `${data.items.length} alertas ativos — ${critical} críticos, ${high} alto, ${moderate} moderado`,
    items: data.items.map((alert) => ({
      id: String(alert.id),
      title: alert.title,
      description: alert.message,
      timeAgo: formatTimeAgo(alert.created_at),
      assessmentId: String(alert.assessment_id),
      riskLevel: alert.severity,
    })),
  };
};
