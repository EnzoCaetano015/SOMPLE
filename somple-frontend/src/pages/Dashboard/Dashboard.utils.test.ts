import { describe, expect, it } from "vite-plus/test";

import { Enum } from "@/api/enums/enum";
import type { GetDashboard } from "@/api/models/dashboard.types";
import {
  DEFAULT_DASHBOARD_FILTERS,
  applyDashboardFilterOptions,
  dashboardFiltersToParams,
  mapDashboardViewModel,
} from "./Dashboard.utils";

const response: GetDashboard.Response = {
  summary: {
    monitored_equipment: 2,
    active_equipment: 2,
    high_risk_equipment: 1,
    active_alerts: 1,
    critical_alerts: 0,
    average_risk_score: 42,
    average_risk_level: Enum.RiskLevel.MEDIUM,
    max_risk_score: 68,
    max_risk_level: Enum.RiskLevel.HIGH,
    assessment_count: 3,
  },
  ranking: [],
  risk_evolution: [],
  risk_distribution: [],
  recent_alerts: [],
  report: {
    average_risk_score: 42,
    max_risk_score: 68,
    assessment_count: 3,
    alert_count: 1,
    counts_by_level: { low: 1, medium: 1, high: 1, critical: 0 },
    evolution: [],
  },
  trends: {
    by_equipment: [
      {
        key: "EQ-001",
        label: "Colheitadeira EQ-001",
        average_risk_score: 51,
        max_risk_score: 68,
        assessment_count: 2,
        alert_count: 1,
      },
    ],
    by_region: [
      {
        key: "7",
        label: "Talhão Oeste",
        average_risk_score: 42,
        max_risk_score: 68,
        assessment_count: 3,
        alert_count: 1,
      },
    ],
    by_operation_category: [
      {
        key: "field",
        label: "Campo",
        average_risk_score: 42,
        max_risk_score: 68,
        assessment_count: 3,
        alert_count: 1,
      },
    ],
  },
};

describe("dashboard mappings", () => {
  it("maps the max score and consolidated report without recalculating risk level", () => {
    const viewModel = mapDashboardViewModel(response);
    expect(viewModel.maxRiskScore).toBe(68);
    expect(viewModel.maxRiskLevel).toBe(Enum.RiskLevel.HIGH);
    expect(viewModel.report.assessmentCount).toBe(3);
    expect(viewModel.trends.byEquipment[0]?.label).toBe("Colheitadeira EQ-001");
    expect(viewModel.trends.byRegion[0]?.label).toBe("Talhão Oeste");
    expect(viewModel.trends.byOperationCategory[0]?.label).toBe("Campo");
  });

  it("preserves empty trend groupings for the dashboard empty states", () => {
    const viewModel = mapDashboardViewModel({
      ...response,
      trends: { by_equipment: [], by_region: [], by_operation_category: [] },
    });
    expect(viewModel.trends).toEqual({
      byEquipment: [],
      byRegion: [],
      byOperationCategory: [],
    });
  });

  it("maps region and category filters to API parameters", () => {
    const filters = DEFAULT_DASHBOARD_FILTERS.map((filter) => ({
      ...filter,
      value:
        filter.id === "region"
          ? "7"
          : filter.id === "operation_category"
            ? "near_water"
            : filter.value,
    }));
    expect(dashboardFiltersToParams(filters)).toEqual({
      period: "7d",
      region_id: 7,
      operation_category: "near_water",
    });
  });

  it("uses filter options returned by the backend", () => {
    const filters = applyDashboardFilterOptions(DEFAULT_DASHBOARD_FILTERS, {
      regions: [{ value: "9", label: "Talhão Oeste" }],
      operation_categories: [{ value: "transport", label: "Transporte" }],
      operation_types: [],
    });
    expect(filters.find((filter) => filter.id === "region")?.options).toContainEqual({
      value: "9",
      label: "Talhão Oeste",
    });
  });
});
