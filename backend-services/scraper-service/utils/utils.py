"""
Utility functions for scraping
"""
from urllib.parse import urlparse
from typing import Dict, Any
import logging

from config import settings

logger = logging.getLogger(__name__)


def detect_platform(url: str) -> str:
    """Detect e-commerce platform from URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    if 'amazon' in domain:
        return 'amazon'
    elif 'flipkart' in domain:
        return 'flipkart'
    elif 'myntra' in domain:
        return 'myntra'
    elif 'ajio' in domain:
        return 'ajio'
    elif 'snapdeal' in domain:
        return 'snapdeal'
    elif 'meesho' in domain:
        return 'meesho'
    elif 'nykaa' in domain:
        return 'nykaa'
    else:
        return 'unknown'


def should_use_manual_scraper(platform: str, force_llm: bool) -> bool:
    """
    Determine if we should use manual scraper or LLM approach
    
    Args:
        platform: Detected platform name
        force_llm: User requested to force LLM scraping
    
    Returns:
        True if manual scraper should be used, False for LLM
    """
    if force_llm:
        return False
    return platform in settings.MANUAL_SCRAPING_PLATFORMS


def calculate_sampling_strategy(total_available: int, max_reviews: int) -> Dict[str, Any]:
    """
    Calculate smart sampling strategy
    
    Strategy:
    - Most recent: 30-40
    - Oldest: 15-20
    - 5-star: 20-25
    - 1-star: 20-25
    - Random middle: 30-40
    """
    if total_available <= max_reviews:
        return {
            "strategy": "all",
            "total": total_available,
        }
    
    # Smart sampling
    return {
        "strategy": "stratified",
        "total": max_reviews,
        "breakdown": {
            "recent": 35,
            "oldest": 20,
            "five_star": 25,
            "one_star": 25,
            "random_middle": 45
        }
    }