from fastapi import APIRouter

from .. import settings
from ..models.health import HealthCheck

router = APIRouter()


@router.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.description,
    }
