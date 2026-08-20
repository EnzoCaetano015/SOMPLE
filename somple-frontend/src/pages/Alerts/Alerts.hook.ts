import { useMemo } from "react";
import { useAppNavigate } from "@/lib/navigation/useAppNavigate";

import { useGetAlerts } from "@/api/controllers/alerts.controller";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";
import { mapAlertsViewModel } from "./Alerts.utils";

export const useAlerts = () => {
  const navigate = useAppNavigate();
  const { isOffline } = useNetworkStatus();

  const { data, isLoading, isError, refetch } = useGetAlerts();

  const viewModel = useMemo(() => {
    if (!data) return null;
    return mapAlertsViewModel(data);
  }, [data]);

  const handleOpenAssessment = (assessmentId: string) => {
    void navigate(`/assessment/${assessmentId}`);
  };

  return {
    ...viewModel,
    isLoading,
    isError,
    isOffline,
    isEmpty: viewModel?.items.length === 0,
    refetch,
    handleOpenAssessment,
  };
};
