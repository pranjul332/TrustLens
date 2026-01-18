"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator
from typing import List, Dict, Optional
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
            
            # Accept any valid URL with http/https scheme
            if parsed.scheme not in ['http', 'https']:
                raise ValueError("URL must use http or https protocol")
            
            # Optional: Log the platform being analyzed
            known_platforms = {
                'amazon.': 'Amazon',
                'flipkart.': 'Flipkart',
                'myntra.': 'Myntra',
                'walmart.': 'Walmart',
                'ebay.': 'eBay',
                'aliexpress.': 'AliExpress',
                'etsy.': 'Etsy',
                'target.': 'Target',
                'bestbuy.': 'Best Buy',
            }
            
            platform = 'Unknown Platform'
            for domain, name in known_platforms.items():
                if domain in parsed.netloc.lower():
                    platform = name
                    break
            
            # Log for analytics (optional)
            # logger.info(f"Analyzing product from: {platform}")
            
            return v
        except ValueError:
            raise
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
    cached: bool = False
    success: bool = True
    trust_score: int
    fake_reviews_percentage: float
    risk_level: str
    score_breakdown: Dict
    key_insights: List[Dict]
    total_reviews_analyzed: int
    recommendation: str
    confidence: float
    timestamp: str