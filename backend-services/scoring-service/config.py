"""
Configuration settings for Scoring Service
"""
from typing import Dict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Component Weights for Trust Score
    NLP_WEIGHT: float = 0.5  # 50% weight to NLP analysis
    BEHAVIOR_WEIGHT: float = 0.3  # 30% weight to behavioral patterns
    STATISTICAL_WEIGHT: float = 0.2  # 20% weight to statistical anomalies
    
    # Statistical Thresholds
    FIVE_STAR_CRITICAL: float = 0.8  # >80% five stars is very suspicious
    FIVE_STAR_WARNING: float = 0.7  # >70% five stars is suspicious
    FIVE_STAR_NOTICE: float = 0.6  # >60% five stars is slightly suspicious
    
    POLARIZATION_CRITICAL: float = 0.7  # >70% polarization
    POLARIZATION_WARNING: float = 0.5  # >50% polarization
    
    MIDDLE_RATIO_THRESHOLD: float = 0.15  # <15% middle ratings is suspicious
    
    # Small Sample Thresholds
    SMALL_SAMPLE_SIZE: int = 20
    SMALL_SAMPLE_FIVE_STAR: float = 0.9  # >90% five stars with small sample
    
    # Confidence Calculation
    BASE_CONFIDENCE: float = 0.5
    LARGE_SAMPLE_SIZE: int = 100
    MEDIUM_SAMPLE_SIZE: int = 50
    SMALL_SAMPLE_SIZE_CONF: int = 20
    
    STRONG_AGREEMENT_THRESHOLD: int = 10  # Score difference
    MODERATE_AGREEMENT_THRESHOLD: int = 20
    
    HIGH_VERIFICATION_RATE: float = 70.0  # >70% is good
    
    # Trust Score Thresholds
    TRUST_EXCELLENT: int = 80  # >=80 is recommended
    TRUST_GOOD: int = 60  # >=60 is caution
    TRUST_POOR: int = 40  # >=40 is not recommended
    # <40 is avoid
    
    # Insight Thresholds
    HIGH_FAKE_PROB: float = 0.6  # >60% average fake probability
    MEDIUM_FAKE_PROB: float = 0.4  # >40% average fake probability
    
    DUPLICATE_THRESHOLD: float = 10.0  # >10% duplicates
    
    UNUSUALLY_POSITIVE: float = 0.85  # >85% positive sentiment
    LOW_TEXT_QUALITY: float = 0.4  # <0.4 quality score
    
    VERY_LOW_VERIFICATION: float = 30.0  # <30% verified
    LOW_VERIFICATION: float = 50.0  # <50% verified
    
    EXTREME_FIVE_STAR: float = 85.0  # >85% five stars
    HIGH_FIVE_STAR: float = 75.0  # >75% five stars
    
    # Max Insights to Return
    MAX_INSIGHTS: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()