"""
Configuration settings for Hybrid Scraper Service
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Scraping Configuration
    MAX_REVIEWS_TO_ANALYZE: int = 150
    REQUEST_TIMEOUT: float = 30.0
    USE_MOCK_SCRAPER: bool = os.getenv("USE_MOCK_SCRAPER", "false").lower() == "true"
    
    # API Keys for LLM Scraping
    SCRAPINGBEE_API_KEY: str = os.getenv("SCRAPINGBEE_API_KEY", "YOUR_API_KEY_HERE")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")
    
    # ScrapingBee Configuration
    SCRAPINGBEE_URL: str = "https://app.scrapingbee.com/api/v1/"
    SCRAPINGBEE_TIMEOUT: float = 60.0
    SCRAPINGBEE_RENDER_JS: bool = True
    SCRAPINGBEE_PREMIUM_PROXY: bool = False
    SCRAPINGBEE_COUNTRY_CODE: str = "in"  # India
    
    # Claude API Configuration
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    CLAUDE_MAX_TOKENS: int = 4000
    CLAUDE_API_VERSION: str = "2023-06-01"
    CLAUDE_TIMEOUT: float = 60.0
    
    # HTML Processing
    MAX_HTML_LENGTH: int = 50000  # Characters to send to LLM
    
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
    MANUAL_SCRAPING_PLATFORMS: List[str] = ["amazon", "flipkart"]
    ALL_SUPPORTED_PLATFORMS: List[str] = [
        "amazon", "flipkart", "myntra", "ajio", 
        "snapdeal", "meesho", "nykaa", "unknown"
    ]
    
    @property
    def is_scrapingbee_configured(self) -> bool:
        """Check if ScrapingBee API is configured"""
        return self.SCRAPINGBEE_API_KEY != "YOUR_API_KEY_HERE"
    
    @property
    def is_anthropic_configured(self) -> bool:
        """Check if Anthropic API is configured"""
        return self.ANTHROPIC_API_KEY != "YOUR_API_KEY_HERE"
    
    @property
    def is_llm_scraping_enabled(self) -> bool:
        """Check if LLM scraping is fully configured"""
        return self.is_scrapingbee_configured and self.is_anthropic_configured
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()