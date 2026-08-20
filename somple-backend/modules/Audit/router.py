from datetime import datetime

from fastapi import APIRouter, Depends, Query

from core.authorization import AuthenticatedUser, require_authenticated_user
from modules.Audit.schemas import AuditResponse
from modules.Audit.service_read import list_audit_history

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("", response_model=AuditResponse, summary="Audit history")
def audit(
    equipment_code: str | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    region_id: int | None = Query(default=None),
    risk_level: str | None = Query(default=None),
    operation_type: str | None = Query(default=None),
    _: AuthenticatedUser = Depends(require_authenticated_user),
) -> AuditResponse:
    return list_audit_history(
        equipment_code=equipment_code,
        start_date=start_date,
        end_date=end_date,
        region_id=region_id,
        risk_level=risk_level,
        operation_type=operation_type,
    )
