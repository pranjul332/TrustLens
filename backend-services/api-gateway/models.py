"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional
from urllib.parse import urlparse


class AnalyzeRequest(BaseModel):
    product_url: str
    force_refresh: Optional[bool] = False
    
    @validator('product_url')
    def validate_url(cls, v):
        """Validate and normalize product URL"""
        try:
            parsed = urlparse(v)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL format")
            
            # Check if it's from supported platforms
            supported_domains = ['amazon.', 'flipkart.', 'myntra.']
            if not any(domain in parsed.netloc.lower() for domain in supported_domains):
                raise ValueError("Unsupported platform. Supported: Amazon, Flipkart, Myntra")
            
            return v
        except Exception as e:
            raise ValueError(f"Invalid product URL: {str(e)}")


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AnalysisResponse(BaseModel):
    status: str
    trust_score: Optional[int] = None
    fake_reviews_percentage: Optional[float] = None
    total_reviews_analyzed: Optional[int] = None
    key_insights: Optional[list] = None
    cached: Optional[bool] = False
    timestamp: Optional[str] = None