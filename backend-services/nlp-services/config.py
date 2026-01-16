"""
Configuration settings for ML-Powered NLP Service
"""
from typing import Set, Dict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # ML Model Configuration
    USE_ML_MODELS: bool = True  # Toggle between rule-based and ML models
    
    # Similarity Detection
    SIMILARITY_THRESHOLD: float = 0.75  # TF-IDF cosine similarity threshold
    JACCARD_THRESHOLD: float = 0.7  # Fallback Jaccard threshold
    
    # TF-IDF Configuration
    TFIDF_MAX_FEATURES: int = 500
    TFIDF_NGRAM_MIN: int = 1
    TFIDF_NGRAM_MAX: int = 3
    TFIDF_MIN_DF: int = 1
    
    # Text Quality Thresholds
    MIN_TEXT_LENGTH: int = 10
    IDEAL_MIN_LENGTH: int = 50
    IDEAL_MAX_LENGTH: int = 200
    MAX_ACCEPTABLE_LENGTH: int = 500
    
    # Readability Targets
    IDEAL_AVG_WORD_LENGTH: float = 5.5
    IDEAL_AVG_SENTENCE_LENGTH: float = 15.0
    
    # Fake Detection Thresholds
    SHORT_REVIEW_LENGTH: int = 10
    HIGH_RISK_THRESHOLD: float = 0.6
    MAX_EXCLAMATION_COUNT: int = 5
    MAX_CAPS_RATIO: float = 0.3
    MIN_LEXICAL_DIVERSITY: float = 0.4
    
    # Feature Weights for ML Fake Detection
    FEATURE_WEIGHTS: Dict[str, float] = {
        'promotional_score': 0.25,
        'generic_score': 0.20,
        'quality_score': -0.15,  # negative = good quality reduces fake score
        'sentiment_rating_mismatch': 0.30,
        'text_features': 0.15,
        'spam_indicators': 0.15
    }
    
    # Sentiment Analysis
    VADER_WEIGHT: float = 0.6
    TEXTBLOB_WEIGHT: float = 0.4
    POSITIVE_THRESHOLD: float = 0.15
    NEGATIVE_THRESHOLD: float = -0.15
    
    # Quality Scoring Weights
    READABILITY_WEIGHT: float = 0.4
    LEXICAL_DIVERSITY_WEIGHT: float = 0.3
    LENGTH_WEIGHT: float = 0.3
    
    # Promotional keywords (for simple scoring)
    PROMOTIONAL_KEYWORDS: Set[str] = {
        'buy', 'purchase', 'deal', 'offer', 'discount', 'sale',
        'recommend', 'must have', 'grab', 'hurry', 'limited'
    }
    
    # Promotional phrases for detection
    PROMOTIONAL_PHRASES: list = [
        'must buy', 'highly recommend', 'best buy', 'grab it', 'don\'t miss',
        'amazing deal', 'worth every penny', 'go for it', 'blindly buy',
        'just buy it', 'buy now', 'genuine product', 'original product',
        'value for money', 'paisa vasool', 'super product', 'best product',
        'excellent choice', 'perfect choice', 'highly satisfied'
    ]
    
    # Generic templates
    GENERIC_TEMPLATES: list = [
        'nice product', 'good product', 'awesome product', 'excellent product',
        'great product', 'superb product', 'amazing product', 'loved it',
        'love it', 'like it', 'satisfied', 'happy with', 'as expected'
    ]
    
    # Spam patterns
    SPAM_PATTERNS: list = [
        r'\b\d{10}\b',  # Phone numbers
        r'whatsapp',
        r'contact.*\d',
        r'click.*link',
        r'visit.*website',
        r'call.*\d',
        r'dm.*me'
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()