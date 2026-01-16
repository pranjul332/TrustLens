"""
Behavior analysis routes
"""
from fastapi import APIRouter, HTTPException, status
import logging

from models import AnalyzeRequest, BehaviorResponse
from pipeline import BehaviorPipeline

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=BehaviorResponse)
async def analyze_behavior(request: AnalyzeRequest):
    """
    Analyze review behavior patterns
    
    Detects:
    - Review bursts (many reviews in short time)
    - Rating spikes
    - Suspicious reviewer patterns
    - Rating distribution anomalies
    - Verification patterns
    
    Returns:
    - Temporal patterns
    - Reviewer patterns
    - Rating distribution
    - Aggregate metrics
    """
    try:
        if not request.reviews:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No reviews provided"
            )
        
        # Initialize pipeline
        pipeline = BehaviorPipeline()
        
        # Run analysis
        result = pipeline.analyze_reviews(request.reviews)
        
        logger.info(
            f"Behavior analysis complete: "
            f"behavior_score={result.aggregate_metrics.get('behavior_fake_score', 0)}"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Behavior analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )