"""
Flipkart product review scraper - Manual/Fast method
"""
from typing import List
from datetime import datetime
import httpx
import random
import logging
from bs4 import BeautifulSoup
from fastapi import HTTPException, status

from models import Review, ProductMetadata, ScrapeResponse
from config import settings

logger = logging.getLogger(__name__)


class FlipkartScraper:
    """Manual scraper for Flipkart - Fast and Free"""
    
    def __init__(self):
        self.base_url = settings.FLIPKART_BASE_URL
    
    async def scrape(self, url: str, max_reviews: int) -> ScrapeResponse:
        """Scrape Flipkart product reviews"""
        start_time = datetime.utcnow()
        logger.info(f"[MANUAL] Scraping Flipkart: {url}")
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                headers = {"User-Agent": random.choice(settings.USER_AGENTS)}
                response = await client.get(url, headers=headers, follow_redirects=True)
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Failed to fetch Flipkart page: {response.status_code}"
                    )
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                metadata = self._extract_metadata(soup)
                reviews = self._extract_reviews(soup, max_reviews)
                
                processing_time = (datetime.utcnow() - start_time).total_seconds()
                
                return ScrapeResponse(
                    success=True,
                    platform="flipkart",
                    scraping_method="manual",
                    product_metadata=metadata,
                    reviews=reviews,
                    total_reviews_scraped=len(reviews),
                    sampling_strategy="recent_reviews",
                    processing_time_seconds=round(processing_time, 2),
                    timestamp=datetime.utcnow().isoformat()
                )
                
        except Exception as e:
            logger.error(f"Flipkart scraping failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Scraping failed: {str(e)}"
            )
    
    def _extract_metadata(self, soup: BeautifulSoup) -> ProductMetadata:
        """Extract Flipkart product metadata"""
        product_name = "Flipkart Product"
        
        # Try multiple possible selectors (Flipkart changes HTML frequently)
        name_elem = (soup.find("span", {"class": "B_NuCI"}) or 
                    soup.find("h1", {"class": "yhB1nd"}) or
                    soup.find("span", {"class": "VU-ZEz"}))
        if name_elem:
            product_name = name_elem.get_text().strip()
        
        avg_rating = None
        rating_elem = soup.find("div", {"class": "_3LWZlK"})
        if rating_elem:
            try:
                avg_rating = float(rating_elem.get_text().strip())
            except:
                pass
        
        return ProductMetadata(
            product_name=product_name,
            platform="flipkart",
            average_rating=avg_rating
        )
    
    def _extract_reviews(self, soup: BeautifulSoup, max_reviews: int) -> List[Review]:
        """Extract Flipkart reviews"""
        reviews = []
        
        # Try multiple possible review container selectors
        review_elements = (soup.find_all("div", {"class": "_1AtVbE"}) or
                          soup.find_all("div", {"class": "col _2wzgFH"}))
        
        for i, elem in enumerate(review_elements[:max_reviews]):
            try:
                rating = 0.0
                rating_elem = elem.find("div", {"class": "_3LWZlK"})
                if rating_elem:
                    try:
                        rating = float(rating_elem.get_text().strip())
                    except:
                        pass
                
                title = None
                title_elem = elem.find("p", {"class": "_2-N8zT"})
                if title_elem:
                    title = title_elem.get_text().strip()
                
                text = ""
                text_elem = elem.find("div", {"class": "t-ZTKy"})
                if text_elem:
                    text = text_elem.get_text().strip()
                
                reviewer_name = None
                name_elem = elem.find("p", {"class": "_2sc7ZR _2V5EHH"})
                if name_elem:
                    reviewer_name = name_elem.get_text().strip()
                
                if text:  # Only add if there's actual review text
                    reviews.append(Review(
                        review_id=f"fk_{i}",
                        reviewer_name=reviewer_name,
                        rating=rating,
                        title=title,
                        text=text,
                        verified_purchase=False
                    ))
            except Exception as e:
                logger.warning(f"Failed to parse Flipkart review: {str(e)}")
                continue
        
        logger.info(f"Extracted {len(reviews)} reviews from Flipkart")
        return reviews