"""
Behavior Service - Main Application Entry Point
Detects suspicious patterns in review behavior and temporal anomalies
"""
from fastapi import FastAPI
import logging

from routes import analysis, health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Behavior Service",
    version="1.0.0",
    description="Behavioral analysis for detecting fake review patterns"
)

# Include routers
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    """Root endpoint with service capabilities"""
    return {
        "service": "Behavior Service",
        "status": "healthy",
        "version": "1.0.0",
        "capabilities": [
            "temporal_pattern_detection",
            "review_burst_detection",
            "reviewer_behavior_analysis",
            "rating_distribution_analysis",
            "verification_analysis"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)