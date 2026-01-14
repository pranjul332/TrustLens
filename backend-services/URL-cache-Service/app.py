"""
URL Cache Service - Main Application Entry Point
"""
from fastapi import FastAPI
import logging

from config import settings
from db.database import startup_db_client, shutdown_db_client
from routes import cache, health, stats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="URL Cache Service",
    version="1.0.0",
    description="Manages product analysis report caching with TTL"
)

# Include routers
app.include_router(cache.router, tags=["Cache"])
app.include_router(health.router, tags=["Health"])
app.include_router(stats.router, tags=["Statistics"])

# Event handlers
app.add_event_handler("startup", startup_db_client)
app.add_event_handler("shutdown", shutdown_db_client)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "URL Cache Service",
        "status": "healthy",
        "version": "1.0.0",
        "cache_ttl_days": settings.CACHE_TTL_DAYS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)