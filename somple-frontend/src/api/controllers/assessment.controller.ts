import { useQuery } from "@tanstack/react-query";

import type { GetAssessment } from "@/api/models/assessment.types";
import { queryKeys } from "@/api/queryKeys";
import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

export const useGetAssessment = (assessmentId: string) => {
  return useQuery({
    queryKey: queryKeys.assessment(assessmentId),
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetAssessment.Response>(
        API_ROUTES.assessments.detail(assessmentId),
      );
      return data;
    },
    enabled: Boolean(assessmentId),
  });
};
