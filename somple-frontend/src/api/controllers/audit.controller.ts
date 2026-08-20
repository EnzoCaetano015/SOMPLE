import { useQuery } from "@tanstack/react-query";

import type { GetAudit } from "@/api/models/audit.types";
import { queryKeys } from "@/api/queryKeys";
import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

export const useGetAudit = (params: GetAudit.Params = {}) => {
  return useQuery({
    queryKey: queryKeys.audit(params),
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetAudit.Response>(API_ROUTES.audit, { params });
      return data;
    },
  });
};
