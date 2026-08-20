import { useQuery } from "@tanstack/react-query";

import type { GetOperations } from "@/api/models/operation.types";
import { queryKeys } from "@/api/queryKeys";
import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

export const useGetOperations = () => {
  return useQuery({
    queryKey: queryKeys.operations,
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetOperations.Response>(API_ROUTES.operations);
      return data;
    },
  });
};
