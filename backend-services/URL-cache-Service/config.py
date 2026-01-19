import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # MongoDB Configuration
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB: str = os.getenv("MONGO_DB")
    CACHE_COLLECTION: str = os.getenv("CACHE_COLLECTION")
    
    # Cache TTL Configuration
    CACHE_TTL_DAYS: int = int(os.getenv("CACHE_TTL_DAYS"))
    
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