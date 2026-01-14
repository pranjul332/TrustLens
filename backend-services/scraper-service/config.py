"""
Configuration settings for Scraper Service
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Scraping Configuration
    MAX_REVIEWS_TO_ANALYZE: int = 150
    REQUEST_TIMEOUT: float = 30.0
    USE_MOCK_SCRAPER: bool = os.getenv("USE_MOCK_SCRAPER", "true").lower() == "true"
    
    # User Agents for rotation
    USER_AGENTS: List[str] = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ]
    
    # Platform URLs
    AMAZON_BASE_URL: str = "https://www.amazon.in"
    FLIPKART_BASE_URL: str = "https://www.flipkart.com"
  
    
    # Supported platforms
    SUPPORTED_PLATFORMS: List[str] = ["amazon", "flipkart", "myntra"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()