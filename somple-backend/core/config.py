from functools import lru_cache
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = Field(alias="APP_ENV", default="development")
    cors_origins: str = Field(alias="CORS_ORIGINS")

    db_host: str = Field(alias="DB_HOST")
    db_port: int = Field(alias="DB_PORT", default=5432)
    db_name: str = Field(alias="DB_NAME")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")
    db_connect_timeout_seconds: int = Field(alias="DB_CONNECT_TIMEOUT_SECONDS", default=5)

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM", default="HS256")
    jwt_exp_hours: int = Field(alias="JWT_EXP_HOURS", default=24)

    model_name: str = Field(alias="MODEL_NAME", default="somple-risk-classifier")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def database_dsn(self) -> str:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return _normalize_database_url(database_url)
        password = quote_plus(self.db_password)
        return (
            f"postgresql://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def jwt_exp_seconds(self) -> int:
        return self.jwt_exp_hours * 3600


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgresql+psycopg://"):
        return url.replace("postgresql+psycopg://", "postgresql://", 1)
    return url


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
