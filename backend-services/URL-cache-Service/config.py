"""
Configuration settings for URL Cache Service
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # MongoDB Configuration
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "fake_review_platform")
    CACHE_COLLECTION: str = "report_cache"
    
    # Cache TTL Configuration
    CACHE_TTL_DAYS: int = int(os.getenv("CACHE_TTL_DAYS", "7"))
    
    # Tracking parameters to remove during URL normalization
    TRACKING_PARAMS: set = {
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
        'ref', 'referrer', 'source', 'campaign', 'gclid', 'fbclid',
        '_encoding', 'psc', 'qid', 'sr', 'keywords', 'ie'
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()