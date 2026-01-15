"""
Configuration settings for NLP Service
"""
from typing import Set
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Similarity Detection
    SIMILARITY_THRESHOLD: float = 0.7  # Jaccard similarity threshold
    
    # Text Quality Thresholds
    MIN_TEXT_LENGTH: int = 10
    IDEAL_MIN_LENGTH: int = 50
    IDEAL_MAX_LENGTH: int = 500
    MAX_ACCEPTABLE_LENGTH: int = 1000
    
    # Fake Detection Thresholds
    SHORT_REVIEW_LENGTH: int = 20
    HIGH_RISK_THRESHOLD: float = 0.6  # Fake probability threshold
    MAX_EXCLAMATION_COUNT: int = 5
    MAX_CAPS_RATIO: float = 0.3
    MAX_WORD_REPETITION: int = 5
    
    # Positive sentiment words
    POSITIVE_WORDS: Set[str] = {
        'excellent', 'great', 'amazing', 'awesome', 'wonderful', 'fantastic',
        'superb', 'outstanding', 'perfect', 'love', 'loved', 'best', 'good',
        'nice', 'happy', 'satisfied', 'recommend', 'quality', 'beautiful',
        'brilliant', 'fabulous', 'impressive', 'exceeded', 'delighted'
    }
    
    # Negative sentiment words
    NEGATIVE_WORDS: Set[str] = {
        'bad', 'terrible', 'horrible', 'worst', 'poor', 'awful', 'disappointing',
        'disappointed', 'waste', 'useless', 'broken', 'defective', 'fake',
        'fraud', 'scam', 'pathetic', 'garbage', 'rubbish', 'regret', 'avoid',
        'never', 'damaged', 'hate', 'hated', 'poor', 'substandard'
    }
    
    # Intensifier words
    INTENSIFIER_WORDS: Set[str] = {
        'very', 'extremely', 'absolutely', 'totally', 'completely',
        'highly', 'really', 'so', 'too', 'quite'
    }
    
    # Promotional keywords
    PROMOTIONAL_KEYWORDS: Set[str] = {
        'buy', 'purchase', 'deal', 'offer', 'discount', 'sale',
        'recommend', 'must have', 'grab', 'hurry', 'limited'
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()