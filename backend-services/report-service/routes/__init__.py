"""
Routes package for Report Service

Combines all route modules into a single router
"""
from fastapi import APIRouter

from .health import router as health_router
from .reports import router as reports_router
from .listing import router as listing_router
from .admin import router as admin_router

# Create main router
router = APIRouter()

# Include all sub-routers
router.include_router(health_router)
router.include_router(reports_router)
router.include_router(listing_router)
router.include_router(admin_router)

__all__ = ["router"]