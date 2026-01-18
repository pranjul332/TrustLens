"""
ML-Powered NLP Service - Main Application Entry Point
Advanced Natural Language Processing using Machine Learning
"""
from fastapi import FastAPI
import logging

from routes import analysis, health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ML-Powered NLP Service",
    version="2.0.0",
    description="Advanced Natural Language Processing using Machine Learning"
)

# Include routers
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    """Root endpoint with ML service capabilities"""
    return {
        "service": "ML-Powered NLP Service",
        "status": "healthy",
        "version": "2.0.0",
        "ml_features": [
            "VADER sentiment analysis",
            "TextBlob sentiment & subjectivity",
            "TF-IDF vectorization",
            "Cosine similarity clustering",
            "Multi-feature fake detection",
            "Advanced text quality metrics",
            "Readability scoring",
            "Lexical diversity analysis"
        ],
        "libraries": ["sklearn", "nltk", "textblob", "numpy", "pandas"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)