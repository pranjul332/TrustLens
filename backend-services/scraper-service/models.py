"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional, List, Dict
from urllib.parse import urlparse

from config import settings


class ScrapeRequest(BaseModel):
    url: str
    max_reviews: Optional[int] = settings.MAX_REVIEWS_TO_ANALYZE
    
    @validator('url')
    def validate_url(cls, v):
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")
        return v


class Review(BaseModel):
    review_id: str
    reviewer_name: Optional[str] = None
    rating: float
    title: Optional[str] = None
    text: str
    date: Optional[str] = None
    verified_purchase: bool = False
    helpful_count: Optional[int] = 0


class ProductMetadata(BaseModel):
    product_name: str
    platform: str
    total_ratings: Optional[int] = None
    average_rating: Optional[float] = None
    rating_distribution: Optional[Dict[str, int]] = None


class ScrapeResponse(BaseModel):
    success: bool
    platform: str
    product_metadata: ProductMetadata
    reviews: List[Review]
    total_reviews_scraped: int
    sampling_strategy: str
    timestamp: str