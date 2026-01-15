"""
Amazon product review scraper - Manual/Fast method
"""
from typing import List, Optional
from datetime import datetime
import httpx
import random
import logging
from bs4 import BeautifulSoup
from fastapi import HTTPException, status

from models import Review, ProductMetadata, ScrapeResponse
from config import settings

logger = logging.getLogger(__name__)


class AmazonScraper:
    """Manual scraper for Amazon - Fast and Free"""
    
    def __init__(self):
        self.base_url = settings.AMAZON_BASE_URL
        
    async def scrape(self, url: str, max_reviews: int) -> ScrapeResponse:
        """Scrape Amazon product reviews"""
        start_time = datetime.utcnow()
        logger.info(f"[MANUAL] Scraping Amazon: {url}")
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                # Get product page
                headers = {"User-Agent": random.choice(settings.USER_AGENTS)}
                response = await client.get(url, headers=headers, follow_redirects=True)
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Failed to fetch Amazon page: {response.status_code}"
                    )
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract product metadata
                metadata = self._extract_metadata(soup)
                
                # Extract reviews
                reviews = self._extract_reviews(soup, max_reviews)
                
                # Calculate processing time
                processing_time = (datetime.utcnow() - start_time).total_seconds()
                
                return ScrapeResponse(
                    success=True,
                    platform="amazon",
                    scraping_method="manual",
                    product_metadata=metadata,
                    reviews=reviews,
                    total_reviews_scraped=len(reviews),
                    sampling_strategy="recent_reviews",
                    processing_time_seconds=round(processing_time, 2),
                    timestamp=datetime.utcnow().isoformat()
                )
                
        except Exception as e:
            logger.error(f"Amazon scraping failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Scraping failed: {str(e)}"
            )
    
    def _extract_metadata(self, soup: BeautifulSoup) -> ProductMetadata:
        """Extract product metadata"""
        # Product name
        product_name = "Unknown Product"
        name_elem = soup.find("span", {"id": "productTitle"})
        if name_elem:
            product_name = name_elem.get_text().strip()
        
        # Average rating
        avg_rating = None
        rating_elem = soup.find("span", {"class": "a-icon-alt"})
        if rating_elem:
            try:
                avg_rating = float(rating_elem.get_text().split()[0])
            except:
                pass
        
        # Total ratings
        total_ratings = None
        ratings_elem = soup.find("span", {"id": "acrCustomerReviewText"})
        if ratings_elem:
            try:
                total_ratings = int(''.join(filter(str.isdigit, ratings_elem.get_text())))
            except:
                pass
        
        # Rating distribution
        rating_distribution = {}
        for i in range(1, 6):
            star_elem = soup.find("a", {"title": f"{i} star"})
            if star_elem:
                percent_text = star_elem.get_text()
                try:
                    percent = int(''.join(filter(str.isdigit, percent_text)))
                    rating_distribution[f"{i}_star"] = percent
                except:
                    pass
        
        return ProductMetadata(
            product_name=product_name,
            platform="amazon",
            total_ratings=total_ratings,
            average_rating=avg_rating,
            rating_distribution=rating_distribution if rating_distribution else None
        )
    
    def _extract_reviews(self, soup: BeautifulSoup, max_reviews: int) -> List[Review]:
        """Extract reviews from product page"""
        reviews = []
        
        try:
            # Find all review elements on the page
            review_elements = soup.find_all("div", {"data-hook": "review"})
            
            for elem in review_elements[:max_reviews]:
                try:
                    review = self._parse_review_element(elem)
                    if review and review.text:  # Only add if there's actual review text
                        reviews.append(review)
                except Exception as e:
                    logger.warning(f"Failed to parse review: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(reviews)} reviews from Amazon")
            return reviews
            
        except Exception as e:
            logger.error(f"Review extraction failed: {str(e)}")
            return reviews
    
    def _parse_review_element(self, elem) -> Optional[Review]:
        """Parse a single review element"""
        try:
            # Review ID
            review_id = elem.get('id', f"amz_{random.randint(1000, 9999)}")
            
            # Reviewer name
            reviewer_name = None
            name_elem = elem.find("span", {"class": "a-profile-name"})
            if name_elem:
                reviewer_name = name_elem.get_text().strip()
            
            # Rating
            rating = 0.0
            rating_elem = elem.find("i", {"data-hook": "review-star-rating"})
            if rating_elem:
                rating_text = rating_elem.get_text()
                try:
                    rating = float(rating_text.split()[0])
                except:
                    pass
            
            # Title
            title = None
            title_elem = elem.find("a", {"data-hook": "review-title"})
            if title_elem:
                title = title_elem.get_text().strip()
            
            # Review text
            text = ""
            text_elem = elem.find("span", {"data-hook": "review-body"})
            if text_elem:
                text = text_elem.get_text().strip()
            
            # Date
            date = None
            date_elem = elem.find("span", {"data-hook": "review-date"})
            if date_elem:
                date = date_elem.get_text().strip()
            
            # Verified purchase
            verified = False
            verified_elem = elem.find("span", {"data-hook": "avp-badge"})
            if verified_elem:
                verified = True
            
            # Helpful count
            helpful_count = 0
            helpful_elem = elem.find("span", {"data-hook": "helpful-vote-statement"})
            if helpful_elem:
                helpful_text = helpful_elem.get_text()
                try:
                    helpful_count = int(''.join(filter(str.isdigit, helpful_text)))
                except:
                    pass
            
            return Review(
                review_id=review_id,
                reviewer_name=reviewer_name,
                rating=rating,
                title=title,
                text=text,
                date=date,
                verified_purchase=verified,
                helpful_count=helpful_count
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse review element: {str(e)}")
            return None