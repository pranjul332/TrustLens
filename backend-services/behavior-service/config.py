"""
Configuration settings for Behavior Service
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Temporal Pattern Detection
    BURST_WINDOW_DAYS: List[int] = [1, 3, 7, 30]
    BURST_MIN_REVIEWS: int = 10
    BURST_MIN_PERCENTAGE: float = 0.3  # 30% of reviews in window
    
    # Rating Spike Detection
    MIN_REVIEWS_FOR_SPIKE: int = 20
    MIN_DAYS_FOR_TEMPORAL: int = 7
    SPIKE_RATING_THRESHOLD: float = 1.0  # Star difference
    MIN_REVIEWS_PER_WEEK: int = 5
    
    # Recency Bias Detection
    RECENCY_DAYS: int = 30
    RECENCY_THRESHOLD: float = 0.5  # 50% of reviews
    
    # Reviewer Pattern Detection
    UNVERIFIED_THRESHOLD: float = 0.7  # 70% unverified is suspicious
    
    # Rating Distribution
    POLARIZATION_THRESHOLD: float = 0.7  # 70% extreme ratings
    HIGH_FIVE_STAR_THRESHOLD: float = 0.7  # 70% five stars
    
    # Behavior Score Weights
    TEMPORAL_WEIGHT: float = 0.4
    REVIEWER_WEIGHT: float = 0.3
    RATING_WEIGHT: float = 0.3
    
    # Date Formats
    DATE_FORMATS: List[str] = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%B %d, %Y",  # January 15, 2026
        "%d %B %Y",   # 15 January 2026
        "%Y/%m/%d",
        "%d/%m/%Y"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()