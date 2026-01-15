"""
NLP analysis routes
"""
from fastapi import APIRouter, HTTPException, status
import logging

from models import AnalyzeRequest, NLPResponse, SentimentRequest, SentimentResponse
from pipeline import NLPPipeline
from analyzers import SentimentAnalyzer

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=NLPResponse)
async def analyze_reviews(request: AnalyzeRequest):
    """
    Analyze reviews for sentiment, fake patterns, and similarity
    
    Returns:
    - Individual review analyses
    - Similarity clusters
    - Aggregate metrics
    """
    try:
        if not request.reviews:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No reviews provided"
            )
        
        # Initialize pipeline
        pipeline = NLPPipeline()
        
        # Run analysis
        result = pipeline.analyze_reviews(request.reviews)
        
        logger.info(
            f"NLP analysis complete: {result.total_reviews} reviews, "
            f"avg fake prob: {result.aggregate_metrics.get('average_fake_probability', 0)}"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"NLP analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """Quick sentiment analysis for a single text"""
    try:
        analyzer = SentimentAnalyzer()
        score, label = analyzer.analyze(request.text)
        
        return SentimentResponse(
            text=request.text[:100],
            sentiment_score=score,
            sentiment_label=label
        )
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sentiment analysis failed: {str(e)}"
        )