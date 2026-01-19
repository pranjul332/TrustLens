"""
Mock scraper for testing without actual web scraping
"""
from datetime import datetime
import random
import logging

from models import Review, ProductMetadata, ScrapeResponse
from utils.utils import detect_platform

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
        
        # Expanded sample texts with mix of genuine and fake-looking reviews
        sample_texts = [
            # Genuine-looking reviews (detailed, specific, balanced)
            "Great product! Highly recommend for daily use.",
            "I've been using this for 3 months now and it's held up really well. The quality is good but the price is a bit high.",
            "Amazing! Worth every penny. Will buy again.",
            "Works exactly as advertised. Shipping took a week which was reasonable. No complaints so far.",
            "Excellent quality and fast shipping.",
            "Good value for money. Happy with my purchase.",
            "Product works as described. No complaints.",
            "Exceeded my expectations! Love it.",
            "The build quality is solid and it does what it's supposed to. Only minor issue is the instructions could be clearer.",
            "Been using this daily for 2 weeks. So far so good, will update if anything changes.",
            "Great product overall. Small learning curve but once you get the hang of it, works perfectly.",
            "Exactly what I needed. Fits perfectly and quality seems durable.",
            "Happy with this purchase. Does exactly what I wanted it to do without any issues.",
            "Quality is decent for the price point. Not premium but gets the job done.",
            "Solid product. Delivery was on time and packaging was secure.",
            "Very satisfied with this purchase. Would recommend to friends.",
            "Good product but took some time to figure out how to use all the features.",
            "Works well and seems durable. Time will tell but initial impressions are positive.",
            "Meets my expectations. Nothing extraordinary but reliable.",
            "Great customer service when I had a question. Product itself works fine.",
            
            # Suspicious/Fake-looking reviews (generic, overly positive/negative, short)
            "Not satisfied with the quality. Expected better.",
            "Decent product but delivery was delayed.",
            "Product is okay but customer service needs improvement.",
            "Best purchase ever! Five stars all the way.",
            "Don't waste your money. Very disappointed.",
            "Average product, nothing special.",
            "Terrible experience, will not buy again.",
            "Perfectly matches the description.",
            "AMAZING PRODUCT!!! BUY NOW!!! BEST EVER!!!",
            "This product changed my life! Can't believe how good it is! 10/10!",
            "Worst product ever. Total scam. DO NOT BUY.",
            "Perfect! Perfect! Perfect! Everything is perfect!",
            "Nice product good quality fast shipping recommended",
            "Very good nice quality I like it very much thank you",
            "Excellent very good super happy with purchase five star",
            "Bad quality terrible do not recommend waste of money",
            "This is the best thing I have ever purchased in my entire life! Revolutionary!",
            "Absolutely horrible. Completely useless. Return immediately.",
            "Good nice very good product happy customer satisfied",
            "5 stars amazing wonderful fantastic incredible best product",
            "Cheap quality broke immediately total waste don't buy",
            "Super duper excellent fabulous marvelous outstanding product wow",
            "Terrible awful horrible disgusting worst purchase ever made",
            "Nice very nice good very good excellent super product",
            "This product is a game changer! Life changing! Must have!",
            "Garbage trash junk waste total ripoff scam fraud",
            "Perfect in every way no flaws whatsoever absolutely flawless",
            "Disaster complete disaster worst experience horrible terrible",
            "Awesome sauce! Totally rad! Super cool! Buy it now!",
            "DO NOT BUY FAKE SCAM WASTE OF MONEY TERRIBLE",
        ]
        
        # Randomly select 30 reviews from the sample texts
        selected_texts = random.sample(sample_texts, min(30, len(sample_texts)))
        
        for i in range(min(max_reviews, len(selected_texts))):
            # Assign ratings with some correlation to sentiment
            text = selected_texts[i]
            
            # Simple heuristic: very positive words -> high rating, negative words -> low rating
            if any(word in text.upper() for word in ["AMAZING", "BEST", "PERFECT", "EXCELLENT", "LOVE", "GAME CHANGER"]):
                rating = random.choice([4.0, 5.0, 5.0, 5.0])
            elif any(word in text.lower() for word in ["terrible", "worst", "scam", "don't buy", "waste", "garbage", "awful"]):
                rating = random.choice([1.0, 1.0, 2.0, 1.0])
            else:
                rating = random.choice([2.0, 3.0, 4.0, 5.0])
            
            reviews.append(Review(
                review_id=f"mock_{i}",
                reviewer_name=f"User{i}",
                rating=rating,
                title=f"Review Title {i}",
                text=text,
                date=f"2026-01-{random.randint(1, 19):02d}",
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