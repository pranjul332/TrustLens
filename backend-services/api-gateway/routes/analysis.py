"""
Analysis routes - Product review analysis endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
import logging
import httpx
import asyncio

from models import AnalyzeRequest, AnalysisResponse
from rate_limiter import check_rate_limit
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_product(
    request: AnalyzeRequest,
    user_id: str = Depends(check_rate_limit)
):
    """
    Main analysis endpoint - orchestrates the entire review analysis pipeline
    """
    logger.info(f"Analysis request from user {user_id} for URL: {request.product_url}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            
            # Step 1: Check cache (URL Cache Service)
            if not request.force_refresh:
                try:
                    cache_response = await client.get(
                        f"{settings.SERVICES['url_cache']}/check-cache",
                        params={"url": request.product_url}
                    )
                    
                    if cache_response.status_code == 200:
                        cached_data = cache_response.json()
                        if cached_data.get("cached") and cached_data.get("valid"):
                            logger.info(f"Cache HIT for {request.product_url}")
                            return AnalysisResponse(
                                status="success",
                                cached=True,
                                **cached_data.get("report", {})
                            )
                    
                    logger.info(f"Cache MISS for {request.product_url}")
                except Exception as e:
                    logger.warning(f"Cache check failed: {str(e)}")
            
            # Step 2: Scrape reviews (Scraper Service)
            logger.info("Initiating scraping...")
            scrape_response = await client.post(
                f"{settings.SERVICES['scraper']}/scrape",
                json={"url": request.product_url}
            )
            
            if scrape_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to scrape product reviews"
                )
            
            reviews_data = scrape_response.json()
            
            # Step 3: Parallel analysis (NLP + Behavior services)
            logger.info("Running parallel analysis...")
            
            nlp_task = client.post(
                f"{settings.SERVICES['nlp']}/analyze",
                json={"reviews": reviews_data.get("reviews", [])}
            )
            
            behavior_task = client.post(
                f"{settings.SERVICES['behavior']}/analyze",
                json={"reviews": reviews_data.get("reviews", [])}
            )
            
            # Wait for both analyses
            nlp_response, behavior_response = await asyncio.gather(
                nlp_task, behavior_task, return_exceptions=True
            )
            
            # Handle potential errors
            if isinstance(nlp_response, Exception) or isinstance(behavior_response, Exception):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Analysis services failed"
                )
            
            nlp_data = nlp_response.json() if nlp_response.status_code == 200 else {}
            behavior_data = behavior_response.json() if behavior_response.status_code == 200 else {}
            
            # Step 4: Generate final score (Scoring Service)
            logger.info("Generating trust score...")
            scoring_response = await client.post(
                f"{settings.SERVICES['scoring']}/calculate-score",
                json={
                    "nlp_results": nlp_data,
                    "behavior_results": behavior_data,
                    "product_metadata": reviews_data.get("metadata", {})
                }
            )
            
            if scoring_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Scoring service failed"
                )
            
            final_score = scoring_response.json()
            
            # Step 5: Store report (Report Service)
            logger.info("Storing report...")
            await client.post(
                f"{settings.SERVICES['report']}/store",
                json={
                    "url": request.product_url,
                    "report": final_score,
                    "ttl_days": 7
                }
            )
            
            # Return final response
            return AnalysisResponse(
                status="success",
                cached=False,
                timestamp=datetime.utcnow().isoformat(),
                **final_score
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )