"""
Scoring calculation routes
"""
from fastapi import APIRouter, HTTPException, status
import logging

from models import ScoreRequest, ScoreResponse
from pipeline import ScoringPipeline

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/calculate-score", response_model=ScoreResponse)
async def calculate_score(request: ScoreRequest):
    """
    Calculate final trust score from NLP, Behavior, and Statistical signals
    
    Combines:
    - NLP fake detection (50% weight)
    - Behavioral patterns (30% weight)
    - Statistical anomalies (20% weight)
    
    Returns:
    - Trust score (0-100, higher = more trustworthy)
    - Risk level (low/medium/high/critical)
    - Detailed insights
    - Purchase recommendation
    - Confidence score
    """
    try:
        # Validate inputs
        if not request.nlp_results or not request.behavior_results:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required analysis results"
            )
        
        # Initialize pipeline
        pipeline = ScoringPipeline()
        
        # Generate final score
        result = pipeline.generate_final_score(
            request.nlp_results,
            request.behavior_results,
            request.product_metadata
        )
        
        logger.info(
            f"Scoring complete: Trust={result.trust_score}, "
            f"Risk={result.risk_level}, "
            f"Insights={len(result.key_insights)}"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scoring failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scoring failed: {str(e)}"
        )