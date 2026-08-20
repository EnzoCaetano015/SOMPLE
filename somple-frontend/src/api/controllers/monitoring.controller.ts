import { useQuery } from "@tanstack/react-query";

import type { GetMonitoring } from "@/api/models/monitoring.types";
import { queryKeys } from "@/api/queryKeys";
import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

export const useGetMonitoring = (params: GetMonitoring.Params = {}) => {
  return useQuery({
    queryKey: queryKeys.monitoring(params.region_id, params.risk_level),
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetMonitoring.Response>(API_ROUTES.monitoring, {
        params,
      });
      return data;
    },
    refetchInterval: 30000,
  });
};
