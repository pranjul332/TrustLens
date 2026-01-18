"""
Scoring Service - Main Application Entry Point
Combines NLP, Behavior, and Statistical signals into final trust score
"""
from fastapi import FastAPI
import logging

from routes import scoring, health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Scoring Service",
    version="1.0.0",
    description="Final trust score calculation and explainability"
)

# Include routers
app.include_router(scoring.router, tags=["Scoring"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    """Root endpoint with service capabilities"""
    return {
        "service": "Scoring Service",
        "status": "healthy",
        "version": "1.0.0",
        "capabilities": [
            "trust_score_calculation",
            "multi_signal_fusion",
            "insight_generation",
            "risk_classification",
            "recommendation_engine"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)