"""
Health check routes
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "service": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }