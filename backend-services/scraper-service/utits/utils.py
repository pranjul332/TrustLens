"""
Utility functions for scraping
"""
from urllib.parse import urlparse
from typing import Dict
import logging

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
    else:
        raise ValueError(f"Unsupported platform: {domain}")


def calculate_sampling_strategy(total_available: int, max_reviews: int) -> Dict[str, int]:
    """
    Calculate how many reviews to scrape from each category
    
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
            "recent": total_available,
            "oldest": 0,
            "five_star": 0,
            "one_star": 0,
            "random": 0
        }
    
    # Smart sampling
    return {
        "strategy": "stratified",
        "total": max_reviews,
        "recent": 35,
        "oldest": 20,
        "five_star": 25,
        "one_star": 25,
        "random": 45  # Fill remaining slots
    }