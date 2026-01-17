"""
Configuration settings for Report Service
"""
import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Service Info
    SERVICE_NAME: str = "Report Service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_DESCRIPTION: str = "Storage and management of analysis reports"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8006
    
    # MongoDB Configuration
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "fake_review_platform")
    REPORTS_COLLECTION: str = "analysis_reports"
    
    # TTL Configuration
    DEFAULT_TTL_DAYS: int = int(os.getenv("DEFAULT_TTL_DAYS", "7"))
    
    # Pagination
    MAX_PAGE_SIZE: int = 100
    DEFAULT_PAGE_SIZE: int = 50
    
    # Valid sort fields
    VALID_SORT_FIELDS: list = ["created_at", "updated_at", "expires_at"]
    DEFAULT_SORT_FIELD: str = "created_at"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()