from core.database import check_database_connection
from ml.runtime import get_model_runtime
from modules.Health.schemas import HealthReadyResponse, HealthResponse


class HealthService:
    @staticmethod
    def get_health() -> HealthResponse:
        return HealthResponse(status="ok")

    @staticmethod
    def get_ready() -> HealthReadyResponse:
        db_ok = check_database_connection()
        runtime = get_model_runtime()
        model_ok = runtime.is_loaded

        status = "ready" if db_ok and model_ok else "not_ready"
        return HealthReadyResponse(
            status=status,
            database="ok" if db_ok else "error",
            model="ok" if model_ok else "error",
            model_version=runtime.model_version if model_ok else None,
        )
