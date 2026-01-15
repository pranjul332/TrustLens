"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse

from config import settings


class ScrapeRequest(BaseModel):
    url: str
    max_reviews: Optional[int] = settings.MAX_REVIEWS_TO_ANALYZE
    force_llm: Optional[bool] = False  # Force LLM mode even for Amazon/Flipkart
    
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
    scraping_method: str  # "manual", "llm", or "mock"
    product_metadata: ProductMetadata
    reviews: List[Review]
    total_reviews_scraped: int
    sampling_strategy: str
    processing_time_seconds: float
    timestamp: str


class LLMExtractionRequest(BaseModel):
    """Request format for LLM extraction"""
    html: str
    platform: str
    max_reviews: int


class LLMExtractionResponse(BaseModel):
    """Response format from LLM extraction"""
    metadata: ProductMetadata
    reviews: List[Review]