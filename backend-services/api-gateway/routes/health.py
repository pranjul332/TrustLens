"""
Health check routes - Monitor service health
"""
from fastapi import APIRouter
from datetime import datetime
import httpx

from config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Check health of all services"""
    service_health = {}
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, service_url in settings.SERVICES.items():
            try:
                response = await client.get(f"{service_url}/health")
                service_health[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time": response.elapsed.total_seconds()
                }
            except Exception as e:
                service_health[service_name] = {
                    "status": "unreachable",
                    "error": str(e)
                }
    
    return {
        "gateway": "healthy",
        "services": service_health,
        "timestamp": datetime.utcnow().isoformat()
    }