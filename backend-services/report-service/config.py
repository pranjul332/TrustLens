"""
Configuration settings for Report Service
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings"""
    
    # Service Info
    SERVICE_NAME: str = os.getenv("SERVICE_NAME")
    SERVICE_VERSION: str = os.getenv("SERVICE_VERSION")
    SERVICE_DESCRIPTION: str = os.getenv("SERVICE_DESCRIPTION")
    
    # Server
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    
    # MongoDB Configuration
    MONGO_URL: str = os.getenv("MONGO_URL")
    MONGO_DB: str = os.getenv("MONGO_DB")
    REPORTS_COLLECTION: str = os.getenv("REPORTS_COLLECTION")
    
    # TTL Configuration
    DEFAULT_TTL_DAYS: int = int(os.getenv("DEFAULT_TTL_DAYS"))
    
    # Pagination
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE"))
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE"))
    
    # Valid sort fields
    VALID_SORT_FIELDS: list = ["created_at", "updated_at", "expires_at"]
    DEFAULT_SORT_FIELD: str = os.getenv("DEFAULT_SORT_FIELD")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")


settings = Settings()