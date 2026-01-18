"""
NLP analysis routes - ML-powered
"""
from fastapi import APIRouter, HTTPException, status
import logging

from models import AnalyzeRequest, NLPResponse, SentimentRequest, SentimentResponse
from pipeline import NLPPipeline
from analyzers import MLSentimentAnalyzer

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=NLPResponse)
async def analyze_reviews(request: AnalyzeRequest):
    """
    ML-powered review analysis
    
    Features:
    - VADER + TextBlob sentiment analysis
    - TF-IDF based similarity detection
    - Multi-feature fake review detection
    - Advanced text quality metrics
    
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
        
        # Initialize ML pipeline
        pipeline = NLPPipeline()
        
        # Run analysis
        result = pipeline.analyze_reviews(request.reviews)
        
        logger.info(
            f"ML Analysis complete: {result.total_reviews} reviews, "
            f"avg fake prob: {result.aggregate_metrics.get('average_fake_probability', 0):.3f}, "
            f"clusters: {len(result.similarity_clusters)}"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ML analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """Quick ML-based sentiment analysis"""
    try:
        analyzer = MLSentimentAnalyzer()
        score, label, confidence = analyzer.analyze(request.text)
        subjectivity = analyzer.get_subjectivity(request.text)
        
        return SentimentResponse(
            text=request.text[:100],
            sentiment_score=score,
            sentiment_label=label,
            confidence=confidence,
            subjectivity=subjectivity
        )
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sentiment analysis failed: {str(e)}"
        )