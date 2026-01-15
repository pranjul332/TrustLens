"""
Hybrid Scraper Service - Main Application Entry Point
Combines manual scrapers (Amazon/Flipkart) with LLM-powered universal scraping
"""
from fastapi import FastAPI
import logging

from config import settings
from routes import scraper, health, platforms

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Hybrid Scraper Service",
    version="2.0.0",
    description="Smart review extraction: Manual scrapers for Amazon/Flipkart, AI-powered for others"
)

# Include routers
app.include_router(scraper.router, tags=["Scraper"])
app.include_router(health.router, tags=["Health"])
app.include_router(platforms.router, tags=["Platforms"])

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Hybrid Scraper Service",
        "version": "2.0.0",
        "status": "healthy",
        "scraping_methods": {
            "manual": {
                "platforms": ["amazon", "flipkart"],
                "speed": "fast (2-5 seconds)",
                "cost": "free",
                "reliability": "good"
            },
            "llm": {
                "platforms": ["any e-commerce site"],
                "speed": "moderate (5-10 seconds)",
                "cost": "free tier: 1000 requests",
                "reliability": "excellent",
                "enabled": settings.is_llm_scraping_enabled
            },
            "mock": {
                "platforms": ["all (testing)"],
                "speed": "instant",
                "cost": "free",
                "enabled": settings.USE_MOCK_SCRAPER
            }
        },
        "max_reviews_per_request": settings.MAX_REVIEWS_TO_ANALYZE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)