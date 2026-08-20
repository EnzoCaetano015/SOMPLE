import { useQuery } from "@tanstack/react-query";

import type { GetEquipmentDetail, GetEquipmentList } from "@/api/models/equipment.types";
import { queryKeys } from "@/api/queryKeys";
import { API_ROUTES } from "@/api/routes";
import { sompleAPI } from "@/lib/config/axios";

export const useGetEquipmentList = (params: GetEquipmentList.Params = {}) => {
  return useQuery({
    queryKey: queryKeys.equipment(params.search, params.region_id, params.risk_level),
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetEquipmentList.Response>(
        API_ROUTES.equipment.list,
        { params },
      );
      return data;
    },
  });
};

export const useGetEquipmentDetail = (equipmentCode: string) => {
  return useQuery({
    queryKey: queryKeys.equipmentDetail(equipmentCode),
    queryFn: async () => {
      const { data } = await sompleAPI.get<GetEquipmentDetail.Response>(
        API_ROUTES.equipment.detail(equipmentCode),
      );
      return data;
    },
    enabled: Boolean(equipmentCode),
  });
};
