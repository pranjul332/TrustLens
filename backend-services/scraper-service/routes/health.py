"""
Health check routes
"""
from fastapi import APIRouter
from datetime import datetime

from config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Detailed health check with configuration status"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "manual_scraping": "enabled",
            "llm_scraping": "enabled" if settings.is_llm_scraping_enabled else "disabled (API keys needed)",
            "mock_scraping": "enabled" if settings.USE_MOCK_SCRAPER else "disabled"
        },
        "configuration": {
            "scrapingbee_configured": settings.is_scrapingbee_configured,
            "OpenAI_configured": settings.is_openai_configured,
            "max_reviews": settings.MAX_REVIEWS_TO_ANALYZE
        }
    }