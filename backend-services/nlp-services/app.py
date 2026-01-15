"""
NLP Service - Main Application Entry Point
Sentiment analysis, fake review detection, and text similarity
"""
from fastapi import FastAPI
import logging

from routes import analysis, health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NLP Service",
    version="1.0.0",
    description="Natural Language Processing for review analysis"
)

# Include routers
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    """Root endpoint with service capabilities"""
    return {
        "service": "NLP Service",
        "status": "healthy",
        "version": "1.0.0",
        "capabilities": [
            "sentiment_analysis",
            "fake_detection",
            "similarity_detection",
            "text_quality_analysis",
            "promotional_scoring"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)