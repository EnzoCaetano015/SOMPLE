from psycopg import Connection

from core.config import settings
from core.security import create_access_token, verify_password
from modules.Auth.repository import AuthRepository
from modules.Auth.schemas import LoginRequest, LoginResponse, UserResponse
from utils.errors import AuthenticationError, ValidationError


class AuthService:
    def __init__(self, conn: Connection):
        self._conn = conn
        self._repository = AuthRepository()

    def login(self, payload: LoginRequest) -> LoginResponse:
        user = self._repository.find_user_by_email(self._conn, payload.email.lower())
        if user is None or not user["is_active"]:
            raise AuthenticationError("Invalid credentials")

        if not verify_password(user["password_hash"], payload.password):
            raise AuthenticationError("Invalid credentials")

        token = create_access_token(
            user_id=user["id"],
            email=user["email"],
            role=user["role"],
        )

        return LoginResponse(
            access_token=token,
            expires_in=settings.jwt_exp_seconds,
            user=UserResponse(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                role=user["role"],
            ),
        )

    @staticmethod
    def validate_login_payload(payload: LoginRequest) -> LoginRequest:
        if not payload.password.strip():
            raise ValidationError("Password is required")
        return payload
