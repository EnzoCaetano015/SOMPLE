import { useMemo, useState } from "react";
import { useAppNavigate } from "@/lib/navigation/useAppNavigate";

import { useGetDashboard } from "@/api/controllers/dashboard.controller";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";
import { ANALYTICAL_ROLES, hasRole } from "@/lib/auth/permissions";
import {
  DEFAULT_DASHBOARD_FILTERS,
  dashboardFiltersToParams,
  mapDashboardViewModel,
  updateDashboardFilter,
} from "./Dashboard.utils";

export const useDashboard = () => {
  const navigate = useAppNavigate();
  const { isOffline } = useNetworkStatus();
  const [filters, setFilters] = useState(DEFAULT_DASHBOARD_FILTERS);
  const params = useMemo(() => dashboardFiltersToParams(filters), [filters]);

  const { data, isLoading, isError, refetch } = useGetDashboard(params);

  const viewModel = useMemo(() => {
    if (!data) return null;
    return mapDashboardViewModel(data, filters);
  }, [data, filters]);

  const handleFilterChange = (filterId: string, value: string) => {
    setFilters((current) => updateDashboardFilter(current, filterId, value));
  };

  const handleAlertDetails = (assessmentId: string) => {
    navigate(`/assessment/${assessmentId}`);
  };

  return {
    ...viewModel,
    isLoading,
    isError,
    isOffline,
    isEmpty: false,
    canViewAssessments: hasRole(...ANALYTICAL_ROLES),
    refetch,
    handleFilterChange,
    handleAlertDetails,
  };
};
