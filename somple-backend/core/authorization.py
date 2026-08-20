from dataclasses import dataclass
from typing import Callable

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import decode_access_token
from utils.errors import AuthenticationError, AuthorizationError

_bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class AuthenticatedUser:
    id: int
    email: str
    role: str


async def get_current_principal(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> AuthenticatedUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError("Missing or invalid authorization header")

    try:
        payload = decode_access_token(credentials.credentials)
    except Exception as exc:
        raise AuthenticationError("Invalid or expired token") from exc

    user_id = payload.get("user_id")
    email = payload.get("sub")
    role = payload.get("role")

    if user_id is None or email is None or role is None:
        raise AuthenticationError("Invalid token payload")

    principal = AuthenticatedUser(id=int(user_id), email=str(email), role=str(role))
    request.state.principal = principal
    return principal


async def require_authenticated_user(
    principal: AuthenticatedUser = Depends(get_current_principal),
) -> AuthenticatedUser:
    return principal


def require_roles(*allowed_roles: str) -> Callable[..., AuthenticatedUser]:
    async def _dependency(
        principal: AuthenticatedUser = Depends(get_current_principal),
    ) -> AuthenticatedUser:
        if principal.role not in allowed_roles:
            raise AuthorizationError("Insufficient permissions")
        return principal

    return _dependency


async def get_current_session(
    principal: AuthenticatedUser = Depends(get_current_principal),
) -> AuthenticatedUser:
    return principal
