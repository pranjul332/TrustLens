from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # JWT
    # JWT_SECRET: str = "your-secret-key-change-in-production"
    # JWT_ALGORITHM: str = "HS256"
    # JWT_EXPIRATION_HOURS: int = 24

    # CORS (STRING, not list)
    CORS_ORIGINS: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60

    # Services
    URL_CACHE_SERVICE: str = "http://url-cache-service:8001"
    SCRAPER_SERVICE: str = "http://scraper-service:8002"
    NLP_SERVICE: str = "http://nlp-service:8003"
    BEHAVIOR_SERVICE: str = "http://behavior-service:8004"
    SCORING_SERVICE: str = "http://scoring-service:8005"
    REPORT_SERVICE: str = "http://report-service:8006"

    @property
    def cors_origins_list(self) -> list[str]:
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

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()