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
        "ml_models_loaded": True,
        "timestamp": datetime.utcnow().isoformat()
    }