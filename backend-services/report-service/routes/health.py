"""
Health check and status endpoints
"""
from fastapi import APIRouter
from datetime import datetime

from ..config import settings
from ..database import ping_database

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """
    Root health check endpoint
    
    Returns basic service information and status
    """
    return {
        "service": settings.SERVICE_NAME,
        "status": "healthy",
        "version": settings.SERVICE_VERSION,
        "default_ttl_days": settings.DEFAULT_TTL_DAYS
    }


@router.get("/health")
async def health_check():
    """
    Detailed health check
    
    Returns service health status and MongoDB connection status
    """
    mongo_connected = await ping_database()
    
    return {
        "service": "healthy",
        "mongodb": "connected" if mongo_connected else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }