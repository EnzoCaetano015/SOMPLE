import { useMemo, useState } from "react";
import { useAppNavigate } from "@/lib/navigation/useAppNavigate";

import { useGetAudit } from "@/api/controllers/audit.controller";
import { useDelayedFilter, useFilterLoading } from "@/lib/hooks/useDelayedFilter";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";
import {
  auditFiltersToParams,
  DEFAULT_AUDIT_FILTERS,
  mapAuditViewModel,
  updateAuditFilter,
} from "./Audit.utils";

export const useAudit = () => {
  const navigate = useAppNavigate();
  const { isOffline } = useNetworkStatus();
  const [filters, setFilters] = useState(DEFAULT_AUDIT_FILTERS);

  const params = useMemo(() => auditFiltersToParams(filters), [filters]);
  const { value: delayedParams, isDelaying } = useDelayedFilter(params);

  const { data, isLoading, isFetching, isError, refetch } = useGetAudit(delayedParams);

  const showSkeleton = useFilterLoading(isDelaying, isLoading, isFetching);

  const viewModel = useMemo(() => {
    if (!data) return null;
    return mapAuditViewModel(data, filters);
  }, [data, filters]);

  const handleFilterChange = (filterId: string, value: string) => {
    setFilters((current) => updateAuditFilter(current, filterId, value));
  };

  const handleOpenAssessment = (assessmentId: string) => {
    void navigate(`/assessment/${assessmentId}`);
  };

  return {
    rows: viewModel?.rows ?? [],
    filters,
    showSkeleton,
    isError,
    isOffline,
    isEmpty: !showSkeleton && (viewModel?.rows.length ?? 0) === 0,
    refetch,
    handleFilterChange,
    handleOpenAssessment,
  };
};
