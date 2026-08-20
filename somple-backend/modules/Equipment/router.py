from fastapi import APIRouter, Depends, Query

from core.authorization import AuthenticatedUser, require_authenticated_user
from modules.Equipment.schemas import EquipmentDetailResponse, EquipmentListResponse
from modules.Equipment.service import get_equipment_detail, list_equipment

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.get("", response_model=EquipmentListResponse, summary="List equipment")
def equipment_list(
    search: str | None = Query(default=None),
    region_id: int | None = Query(default=None),
    risk_level: str | None = Query(default=None),
    _: AuthenticatedUser = Depends(require_authenticated_user),
) -> EquipmentListResponse:
    return list_equipment(search=search, region_id=region_id, risk_level=risk_level)


@router.get("/{equipment_code}", response_model=EquipmentDetailResponse, summary="Equipment detail")
def equipment_detail(
    equipment_code: str,
    _: AuthenticatedUser = Depends(require_authenticated_user),
) -> EquipmentDetailResponse:
    return get_equipment_detail(equipment_code)
