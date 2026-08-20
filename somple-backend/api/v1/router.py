from fastapi import APIRouter

from modules.Alerts.router import router as alerts_router
from modules.Assessment.router import router as assessments_router
from modules.Audit.router import router as audit_router
from modules.Auth.router import router as auth_router
from modules.Dashboard.router import router as dashboard_router
from modules.Equipment.router import router as equipment_router
from modules.Health.router import router as health_router
from modules.Monitoring.router import router as monitoring_router
from modules.Operations.router import router as operations_router
from modules.Telemetry.router import router as telemetry_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(dashboard_router)
router.include_router(monitoring_router)
router.include_router(equipment_router)
router.include_router(operations_router)
router.include_router(telemetry_router)
router.include_router(assessments_router)
router.include_router(alerts_router)
router.include_router(audit_router)
