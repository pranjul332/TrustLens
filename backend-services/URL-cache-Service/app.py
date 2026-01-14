"""
URL Cache Service - Main Application Entry Point
"""
from fastapi import FastAPI
import logging

from config import settings
from routes import  health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="URL Cache Service",
    version="1.0.0",
    description="Manages product analysis report caching with TTL"
)

app.include_router(health.router, tags=["Health"])

# Event handlers

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