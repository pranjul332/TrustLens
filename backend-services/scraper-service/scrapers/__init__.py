"""
Scrapers package initialization
"""
from .amazon import AmazonScraper
from .flipkart import FlipkartScraper
from .llm import UniversalLLMScraper
from .mock import MockScraper

__all__ = ["AmazonScraper", "FlipkartScraper", "UniversalLLMScraper", "MockScraper"]