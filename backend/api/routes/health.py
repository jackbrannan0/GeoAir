"""Health check and status endpoints"""

from fastapi import APIRouter, Depends
from backend.core.config import settings
from backend.schemas import HealthCheck

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(version=settings.app_version)


@router.get("/status", response_model=dict)
async def status():
    """Application status endpoint"""
    return {
        "status": "running",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }
