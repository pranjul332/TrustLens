"""
API Gateway Service - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config import settings
# from routes import auth, analysis, health  # Original import
from routes import analysis, health  # Auth commented out for now

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Fake Review Intelligence API Gateway",
    version="1.0.0",
    description="Central gateway for product review analysis"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])  # Auth disabled for now
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    """Root endpoint"""
    from datetime import datetime
    return {
        "service": "API Gateway",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)