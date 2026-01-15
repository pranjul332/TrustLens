"""
Mock scraper for testing without actual web scraping
"""
from datetime import datetime
import random
import logging

from models import Review, ProductMetadata, ScrapeResponse
from utils import detect_platform

logger = logging.getLogger(__name__)


class MockScraper:
    """Mock scraper for testing without actual web scraping"""
    
    async def scrape(self, url: str, max_reviews: int) -> ScrapeResponse:
        """Generate mock review data"""
        start_time = datetime.utcnow()
        logger.info(f"[MOCK] Using mock scraper for: {url}")
        
        platform = detect_platform(url)
        
        # Generate mock reviews
        reviews = []
        sample_texts = [
            "Great product! Highly recommend for daily use.",
            "Not satisfied with the quality. Expected better.",
            "Amazing! Worth every penny. Will buy again.",
            "Decent product but delivery was delayed.",
            "Excellent quality and fast shipping.",
            "Product is okay but customer service needs improvement.",
            "Best purchase ever! Five stars all the way.",
            "Don't waste your money. Very disappointed.",
            "Good value for money. Happy with my purchase.",
            "Product works as described. No complaints.",
            "Quality could be better for the price.",
            "Exceeded my expectations! Love it.",
            "Average product, nothing special.",
            "Terrible experience, will not buy again.",
            "Perfectly matches the description."
        ]
        
        for i in range(min(max_reviews, 50)):
            rating = random.choice([1.0, 2.0, 3.0, 4.0, 5.0])
            reviews.append(Review(
                review_id=f"mock_{i}",
                reviewer_name=f"User{i}",
                rating=rating,
                title=f"Review Title {i}",
                text=random.choice(sample_texts),
                date=f"2026-01-{random.randint(1, 13)}",
                verified_purchase=random.choice([True, False]),
                helpful_count=random.randint(0, 50)
            ))
        
        metadata = ProductMetadata(
            product_name="Mock Product for Testing",
            platform=platform,
            total_ratings=500,
            average_rating=4.2,
            rating_distribution={
                "5_star": 60,
                "4_star": 20,
                "3_star": 10,
                "2_star": 5,
                "1_star": 5
            }
        )
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return ScrapeResponse(
            success=True,
            platform=platform,
            scraping_method="mock",
            product_metadata=metadata,
            reviews=reviews,
            total_reviews_scraped=len(reviews),
            sampling_strategy="mock_random",
            processing_time_seconds=round(processing_time, 2),
            timestamp=datetime.utcnow().isoformat()
        )