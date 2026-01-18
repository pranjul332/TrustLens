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
async def calculate_score(request: dict):  # ← Changed to dict temporarily
    """
    Calculate final trust score from NLP, Behavior, and Statistical signals
    """
    try:
        # Log the raw incoming data
        logger.info(f"Raw request keys: {request.keys()}")
        logger.info(f"NLP results keys: {request.get('nlp_results', {}).keys() if isinstance(request.get('nlp_results'), dict) else 'NOT A DICT'}")
        logger.info(f"Behavior results keys: {request.get('behavior_results', {}).keys() if isinstance(request.get('behavior_results'), dict) else 'NOT A DICT'}")
        logger.info(f"Product metadata keys: {request.get('product_metadata', {}).keys() if isinstance(request.get('product_metadata'), dict) else 'NOT A DICT'}")
        
        # Try to parse with Pydantic
        try:
            score_request = ScoreRequest(**request)
            logger.info("✅ Pydantic validation passed!")
        except Exception as e:
            logger.error(f"❌ Pydantic validation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        
        # Initialize pipeline
        pipeline = ScoringPipeline()
        
        # Generate final score
        result = pipeline.generate_final_score(
            score_request.nlp_results,
            score_request.behavior_results,
            score_request.product_metadata
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