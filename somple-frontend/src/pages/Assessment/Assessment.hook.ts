import { useMemo } from "react";
import { useParams } from "react-router";

import { useGetAssessment } from "@/api/controllers/assessment.controller";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";
import { mapAssessmentViewModel } from "./Assessment.utils";

export const useAssessment = () => {
  const { assessmentId = "" } = useParams();
  const { isOffline } = useNetworkStatus();

  const { data, isLoading, isError, refetch } = useGetAssessment(assessmentId);

  const assessment = useMemo(() => mapAssessmentViewModel(data), [data]);

  return {
    assessment,
    isLoading,
    isError,
    isOffline,
    isEmpty: !isLoading && !assessment,
    refetch,
  };
};
