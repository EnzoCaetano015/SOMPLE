import { useMemo } from "react";
import { useParams } from "react-router";

import { useGetEquipmentDetail } from "@/api/controllers/equipment.controller";
import { useNetworkStatus } from "@/lib/hooks/useNetworkStatus.hook";
import { mapEquipmentDetailViewModel } from "./EquipmentDetail.utils";

export const useEquipmentDetail = () => {
  const { equipmentId = "" } = useParams();
  const { isOffline } = useNetworkStatus();

  const { data, isLoading, isError, refetch } = useGetEquipmentDetail(equipmentId);

  const equipment = useMemo(() => mapEquipmentDetailViewModel(data), [data]);

  return {
    equipment,
    isLoading,
    isError,
    isOffline,
    isEmpty: !isLoading && !equipment,
    refetch,
  };
};
