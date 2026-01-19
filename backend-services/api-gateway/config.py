from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str
    
    # CORS (STRING, not list)
    CORS_ORIGINS: str
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW: int

    # Service URLs
    URL_CACHE_SERVICE: str
    SCRAPER_SERVICE: str
    NLP_SERVICE: str
    BEHAVIOR_SERVICE: str
    SCORING_SERVICE: str
    REPORT_SERVICE: str

    @property
    def cors_origins_list(self) -> list[str]:
        """Convert comma-separated CORS origins to list"""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def SERVICES(self) -> dict[str, str]:
        """Dictionary of service URLs for easy access"""
        return {
            'url_cache': self.URL_CACHE_SERVICE,
            'scraper': self.SCRAPER_SERVICE,
            'nlp': self.NLP_SERVICE,
            'behavior': self.BEHAVIOR_SERVICE,
            'scoring': self.SCORING_SERVICE,
            'report': self.REPORT_SERVICE
        }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

settings = Settings()