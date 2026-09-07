from fastapi import APIRouter, Depends

from core.authorization import AuthenticatedUser, require_roles
from modules.Operations.schemas import OperationsResponse
from modules.Operations.service import list_operations

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get("", response_model=OperationsResponse, summary="List operations")
def operations(
    _: AuthenticatedUser = Depends(require_roles("admin", "analyst", "operator")),
) -> OperationsResponse:
    return list_operations()
