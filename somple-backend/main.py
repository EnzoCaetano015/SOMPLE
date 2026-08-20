from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from api.v1.router import router as api_v1_router
from core.config import settings
from core.database import close_database_pool, init_database_pool
from core.observability import register_observability
from ml.runtime import get_model_runtime
from utils.errors import register_exception_handlers

OPENAPI_TAGS = [
    {"name": "Healthcheck", "description": "Health and readiness probes."},
    {"name": "Auth", "description": "Authentication endpoints."},
    {"name": "Dashboard", "description": "Dashboard KPIs and charts."},
    {"name": "Monitoring", "description": "Live equipment monitoring."},
    {"name": "Equipment", "description": "Equipment fleet management."},
    {"name": "Operations", "description": "Operational groupings."},
    {"name": "Telemetry", "description": "Telemetry ingestion and risk pipeline."},
    {"name": "Risk Assessments", "description": "Risk assessment details."},
    {"name": "Alerts", "description": "Alert center."},
    {"name": "Audit", "description": "Audit trail and history."},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database_pool()
    try:
        get_model_runtime().load()
    except Exception:
        pass
    yield
    close_database_pool()


app = FastAPI(
    title="SOMPLE API",
    description=(
        "API de monitoramento e predição de riscos ambientais e "
        "operacionais para equipamentos agrícolas."
    ),
    version="1.0.0",
    openapi_tags=OPENAPI_TAGS,
    lifespan=lifespan,
)

register_observability(app)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    for path, methods in schema.get("paths", {}).items():
        if path.startswith("/api/v1") and not _is_public_path(path):
            for operation in methods.values():
                operation.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = schema
    return app.openapi_schema


def _is_public_path(path: str) -> bool:
    public_suffixes = ("/health", "/auth/login")
    return any(path.endswith(suffix) for suffix in public_suffixes)


app.openapi = custom_openapi
