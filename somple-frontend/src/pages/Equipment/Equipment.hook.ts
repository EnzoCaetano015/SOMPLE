import { useMemo, useState } from "react";
import { useAppNavigate } from "@/lib/navigation/useAppNavigate";

import { useGetEquipmentList } from "@/api/controllers/equipment.controller";
import { useDelayedFilter, useFilterLoading } from "@/lib/hooks/useDelayedFilter";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";
import type { EquipmentViewModel } from "./Equipment.types";
import {
  DEFAULT_EQUIPMENT_FILTERS,
  equipmentFiltersToParams,
  mapEquipmentItems,
} from "./Equipment.utils";

export const useEquipment = () => {
  const navigate = useAppNavigate();
  const { isOffline } = useNetworkStatus();
  const [searchQuery, setSearchQuery] = useState("");
  const [regionFilter, setRegionFilter] = useState("all");
  const [riskFilter, setRiskFilter] = useState("all");
  const [viewMode, setViewMode] = useState<EquipmentViewModel["viewMode"]>("cards");

  const { value: searchWithDelay, isDelaying: isSearchDelaying } = useDelayedFilter(searchQuery);
  const { value: regionWithDelay, isDelaying: isRegionDelaying } = useDelayedFilter(regionFilter);
  const { value: riskWithDelay, isDelaying: isRiskDelaying } = useDelayedFilter(riskFilter);
  const isDelaying = isSearchDelaying || isRegionDelaying || isRiskDelaying;

  const params = useMemo(
    () => equipmentFiltersToParams(searchWithDelay, regionWithDelay, riskWithDelay),
    [searchWithDelay, regionWithDelay, riskWithDelay],
  );

  const { data, isLoading, isFetching, isError, refetch } = useGetEquipmentList(params);

  const showSkeleton = useFilterLoading(isDelaying, isLoading, isFetching);

  const filters = useMemo(
    () =>
      DEFAULT_EQUIPMENT_FILTERS.map((filter) => ({
        ...filter,
        value:
          filter.id === "region" ? regionFilter : filter.id === "risk" ? riskFilter : filter.value,
      })),
    [regionFilter, riskFilter],
  );

  const items = useMemo(() => (data ? mapEquipmentItems(data) : []), [data]);
  const totalLabel = data ? `${data.total} equipamentos cadastrados` : undefined;

  const handleSearchChange = (value: string) => {
    setSearchQuery(value);
  };

  const handleViewModeChange = (mode: EquipmentViewModel["viewMode"]) => {
    setViewMode(mode);
  };

  const handleFilterChange = (filterId: string, value: string) => {
    if (filterId === "region") setRegionFilter(value);
    if (filterId === "risk") setRiskFilter(value);
  };

  const handleSelectEquipment = (equipmentId: string) => {
    navigate(`/equipment/${equipmentId}`);
  };

  return {
    totalLabel,
    searchQuery,
    viewMode,
    filters,
    items,
    showSkeleton,
    isError,
    isOffline,
    isEmpty: !showSkeleton && items.length === 0,
    refetch,
    handleSearchChange,
    handleViewModeChange,
    handleFilterChange,
    handleSelectEquipment,
  };
};
