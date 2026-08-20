from fastapi import APIRouter, Depends, Request, status

from core.authorization import AuthenticatedUser, require_authenticated_user
from core.database import Database
from modules.Audit.service import AuditService
from modules.Auth.schemas import LoginRequest, LoginResponse
from modules.Auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse, summary="Authenticate user")
def login(payload: LoginRequest, request: Request) -> LoginResponse:
    AuthService.validate_login_payload(payload)
    with Database.session() as conn:
        response = AuthService(conn).login(payload)
        AuditService(conn).log_event(
            event_type="auth.login",
            actor_user_id=response.user.id,
            request=request,
            entity_type="user",
            entity_id=response.user.id,
            status_code=200,
            metadata={"email": response.user.email},
        )
        conn.commit()
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Logout user")
def logout(
    request: Request,
    user: AuthenticatedUser = Depends(require_authenticated_user),
) -> None:
    with Database.session() as conn:
        AuditService(conn).log_event(
            event_type="auth.logout",
            actor_user_id=user.id,
            request=request,
            entity_type="user",
            entity_id=user.id,
            status_code=204,
            metadata={"email": user.email},
        )
        conn.commit()
