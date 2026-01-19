"""
Analysis routes - Product review analysis endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
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
    http_request: Request,
    _: None = Depends(check_rate_limit)
):
    """
    Main analysis endpoint - orchestrates the entire review analysis pipeline
    NOTE: Currently using MOCK scraping for testing. Switch to /scrape for production.
    Authentication disabled for testing, but rate limiting still active.
    """
    client_ip = http_request.client.host
    logger.info(f"Analysis request from {client_ip} for URL: {request.product_url}")
    
    try:
        # FIXED: Increased timeout to 120s (LLM scraping can take 60+ seconds)
        async with httpx.AsyncClient(timeout=120.0) as client:
            
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
                f"{settings.SERVICES['scraper']}/scrape/mock",
                json={"url": request.product_url}
            )
            
            if scrape_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Failed to scrape product reviews: {scrape_response.text}"
                )
            
            reviews_data = scrape_response.json()
            logger.info(f"Successfully scraped {len(reviews_data.get('reviews', []))} reviews (MOCK DATA)")
            
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
            if isinstance(nlp_response, Exception):
                logger.error(f"NLP service failed: {str(nlp_response)}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"NLP analysis failed: {str(nlp_response)}"
                )
            
            if isinstance(behavior_response, Exception):
                logger.error(f"Behavior service failed: {str(behavior_response)}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Behavior analysis failed: {str(behavior_response)}"
                )
            
            nlp_data = nlp_response.json() if nlp_response.status_code == 200 else {}
            behavior_data = behavior_response.json() if behavior_response.status_code == 200 else {}
            
            logger.info(f"NLP Data: {nlp_data}")
            logger.info(f"Behavior Data: {behavior_data}")
            
            # Step 4: Generate final score (Scoring Service)
            logger.info("Generating trust score...")
            
            scoring_payload = {
                "nlp_results": nlp_data,  # Send the entire NLP response
    			"behavior_results": behavior_data,  # Send the entire Behavior response
    			"product_metadata": {
        			"product_name": reviews_data.get("product_metadata", {}).get("product_name", "Unknown Product"),
        			"platform": reviews_data.get("product_metadata", {}).get("platform", "unknown"),
        			"total_ratings": reviews_data.get("product_metadata", {}).get("total_ratings"),
        			"average_rating": reviews_data.get("product_metadata", {}).get("average_rating"),
        			"rating_distribution": behavior_data.get("rating_distribution", {})
    			}
            }
            
            logger.info(f"Scoring payload keys: {scoring_payload.keys()}")
            
            scoring_response = await client.post(
                f"{settings.SERVICES['scoring']}/calculate-score",
                json=scoring_payload
            )
            
            if scoring_response.status_code != 200:
                logger.error(f"Scoring error: {scoring_response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Scoring service failed: {scoring_response.text}"
                )
            
            final_score = scoring_response.json()
            
            # Step 5: Store report (Report Service)
            logger.info("Storing report...")
            await client.post(
                f"{settings.SERVICES['report']}/reports/store",
                json={
                    "url": request.product_url,
                    "report": final_score,
                    "ttl_days": 7
                }
            )
            
            timestamp = final_score.pop('timestamp', None) or datetime.utcnow().isoformat()
            
            # Return final response
            return AnalysisResponse(
                status="success",
    			cached=False,
    			timestamp=final_score.get('timestamp', datetime.utcnow().isoformat()),
    			success=final_score.get('success', True),
    			trust_score=final_score['trust_score'],
    			fake_reviews_percentage=final_score['fake_reviews_percentage'],
    			risk_level=final_score['risk_level'],
    			score_breakdown=final_score['score_breakdown'],
    			key_insights=final_score['key_insights'],
    			total_reviews_analyzed=final_score['total_reviews_analyzed'],
    			recommendation=final_score['recommendation'],
    			confidence=final_score['confidence']
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )