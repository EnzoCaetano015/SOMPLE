import { useQuery } from "@tanstack/react-query";

import type { GetDashboard, GetDashboardFilterOptions } from "@/api/models/dashboard.types";
import { queryKeys } from "@/api/queryKeys";
import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

export const useGetDashboard = (params: GetDashboard.Params = {}) => {
  return useQuery({
    queryKey: queryKeys.dashboard(
      params.period,
      params.region_id,
      params.operation_category,
      params.operation_type,
    ),
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetDashboard.Response>(API_ROUTES.dashboard.summary, {
        params,
      });
      return data;
    },
  });
};

export const useGetDashboardFilterOptions = () =>
  useQuery({
    queryKey: queryKeys.dashboardFilterOptions,
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetDashboardFilterOptions.Response>(
        API_ROUTES.dashboard.filterOptions,
      );
      return data;
    },
  });
