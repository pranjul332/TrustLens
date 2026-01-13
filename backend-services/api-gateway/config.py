"""
Configuration settings for API Gateway
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # JWT Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000",]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10 
    RATE_LIMIT_WINDOW: int = 60 
    
    # Service URLs
    URL_CACHE_SERVICE: str = os.getenv("URL_CACHE_SERVICE", "http://url-cache-service:8001")
    SCRAPER_SERVICE: str = os.getenv("SCRAPER_SERVICE", "http://scraper-service:8002")
    NLP_SERVICE: str = os.getenv("NLP_SERVICE", "http://nlp-service:8003")
    BEHAVIOR_SERVICE: str = os.getenv("BEHAVIOR_SERVICE", "http://behavior-service:8004")
    SCORING_SERVICE: str = os.getenv("SCORING_SERVICE", "http://scoring-service:8005")
    REPORT_SERVICE: str = os.getenv("REPORT_SERVICE", "http://report-service:8006")
    
    @property
    def SERVICES(self) -> dict:
        """Get all service URLs as a dictionary"""
        return {
            "url_cache": self.URL_CACHE_SERVICE,
            "scraper": self.SCRAPER_SERVICE,
            "nlp": self.NLP_SERVICE,
            "behavior": self.BEHAVIOR_SERVICE,
            "scoring": self.SCORING_SERVICE,
            "report": self.REPORT_SERVICE,
        }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()