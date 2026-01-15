"""
Main scraping routes with hybrid approach
"""
from fastapi import APIRouter, HTTPException, status
import logging

from models import ScrapeRequest, ScrapeResponse
from utils.utils import detect_platform, should_use_manual_scraper
from config import settings
from scrapers import AmazonScraper, FlipkartScraper, UniversalLLMScraper, MockScraper

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_reviews(request: ScrapeRequest):
    """
    Scrape product reviews with hybrid approach:
    - Amazon/Flipkart: Fast manual scraping (free)
    - Other sites: AI-powered universal scraping (ScrapingBee + ChatGPT)
    - Mock mode: Testing without external requests
    
    Set force_llm=true to use LLM scraping for Amazon/Flipkart
    """
    try:
        # Detect platform
        platform = detect_platform(request.url)
        logger.info(f"Platform detected: {platform}")
        
        # Check if using mock scraper
        if settings.USE_MOCK_SCRAPER:
            logger.info(f"Using MOCK scraper (testing mode)")
            scraper = MockScraper()
            return await scraper.scrape(request.url, request.max_reviews)
        
        # Decide scraping method
        use_manual = should_use_manual_scraper(platform, request.force_llm)
        
        if use_manual:
            # Use fast manual scrapers for Amazon/Flipkart
            if platform == 'amazon':
                logger.info(f"Using MANUAL scraper for Amazon")
                scraper = AmazonScraper()
            elif platform == 'flipkart':
                logger.info(f"Using MANUAL scraper for Flipkart")
                scraper = FlipkartScraper()
            else:
                raise ValueError(f"Manual scraper not available for {platform}")
            
            return await scraper.scrape(request.url, request.max_reviews)
        else:
            # Use LLM-powered universal scraper for other platforms
            logger.info(f"Using LLM scraper for {platform}")
            
            # Check if LLM scraping is configured
            if not settings.is_llm_scraping_enabled:
                missing = []
                if not settings.is_scrapingbee_configured:
                    missing.append("SCRAPINGBEE_API_KEY")
                if not settings.is_openai_configured:
                    missing.append("OPENAI_API_KEY")
                
                raise HTTPException(
                    status_code=status.HTTP_501_NOT_IMPLEMENTED,
                    detail=f"LLM scraping not configured. Missing: {', '.join(missing)}"
                )
            
            scraper = UniversalLLMScraper()
            return await scraper.scrape(request.url, request.max_reviews, platform)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Scraping failed with stacktrace")
        raise HTTPException(
        status_code=500,
        detail="Scraping failed. Check server logs."
    )