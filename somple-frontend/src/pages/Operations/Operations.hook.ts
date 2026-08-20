import { useMemo } from "react";

import { useGetOperations } from "@/api/controllers/operations.controller";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";
import { mapOperationsViewModel } from "./Operations.utils";

export const useOperations = () => {
  const { isOffline } = useNetworkStatus();

  const { data, isLoading, isError, refetch } = useGetOperations();

  const viewModel = useMemo(() => {
    if (!data) return null;
    return mapOperationsViewModel(data);
  }, [data]);

  return {
    ...viewModel,
    isLoading,
    isError,
    isOffline,
    isEmpty: viewModel?.items.length === 0,
    refetch,
  };
};
