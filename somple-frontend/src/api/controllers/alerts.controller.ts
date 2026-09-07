import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import type { GetAlerts, UpdateAlertStatus } from "@/api/models/alert.types";
import { queryKeys } from "@/api/queryKeys";
import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

export const useGetAlerts = (params: GetAlerts.Params = {}) => {
  return useQuery({
    queryKey: queryKeys.alerts(params.status, params.severity),
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetAlerts.Response>(API_ROUTES.alerts.list, {
        params,
      });
      return data;
    },
  });
};

export const useUpdateAlertStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      id,
      status,
    }: {
      id: number;
      status: UpdateAlertStatus.Request["status"];
    }) => {
      const { data } = await sompleAPI.patch<UpdateAlertStatus.Response>(
        API_ROUTES.alerts.status(id),
        { status },
      );
      return data;
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["alerts"] });
    },
  });
};
