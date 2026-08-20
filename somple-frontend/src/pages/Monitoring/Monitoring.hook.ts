import { useMemo, useState } from "react";



import { useGetMonitoring } from "@/api/controllers/monitoring.controller";

import { useDelayedFilter, useFilterLoading } from "@/lib/hooks/useDelayedFilter";

import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";

import {

  DEFAULT_MONITORING_FILTERS,

  mapMonitoringViewModel,

  monitoringFiltersToParams,

} from "./Monitoring.utils";



export const useMonitoring = () => {

  const { isOffline } = useNetworkStatus();

  const [regionFilter, setRegionFilter] = useState("all");

  const [statusFilter, setStatusFilter] = useState("all");



  const { value: regionWithDelay, isDelaying: isRegionDelaying } = useDelayedFilter(regionFilter);

  const { value: statusWithDelay, isDelaying: isStatusDelaying } = useDelayedFilter(statusFilter);

  const isDelaying = isRegionDelaying || isStatusDelaying;



  const params = useMemo(

    () => monitoringFiltersToParams(regionWithDelay, statusWithDelay),

    [regionWithDelay, statusWithDelay],

  );



  const { data, isLoading, isFetching, isError, refetch } = useGetMonitoring(params);



  const showSkeleton = useFilterLoading(isDelaying, isLoading, isFetching);



  const filters = useMemo(

    () =>

      DEFAULT_MONITORING_FILTERS.map((filter) => ({

        ...filter,

        value:

          filter.id === "region"

            ? regionFilter

            : filter.id === "status"

              ? statusFilter

              : filter.value,

      })),

    [regionFilter, statusFilter],

  );



  const viewModel = useMemo(() => {

    if (!data) return null;

    return mapMonitoringViewModel(data, regionFilter, statusFilter);

  }, [data, regionFilter, statusFilter]);



  const handleFilterChange = (filterId: string, value: string) => {

    if (filterId === "region") {

      setRegionFilter(value);

      return;

    }



    if (filterId === "status") {

      setStatusFilter(value);

    }

  };



  return {

    summary: viewModel?.summary,

    filters,

    rows: viewModel?.rows ?? [],

    showSkeleton,

    isError,

    isOffline,

    isEmpty: !showSkeleton && (viewModel?.rows.length ?? 0) === 0,

    refetch,

    handleFilterChange,

  };

};

