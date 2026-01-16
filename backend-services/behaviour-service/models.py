"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class Review(BaseModel):
    review_id: str
    rating: float
    text: str
    date: Optional[str] = None
    reviewer_name: Optional[str] = None
    verified_purchase: bool = False


class AnalyzeRequest(BaseModel):
    reviews: List[Review]


class TemporalPattern(BaseModel):
    pattern_type: str  # burst, spike, gradual_increase, recency_bias
    time_window: str
    review_count: int
    average_rating: float
    suspicion_score: float
    description: str


class ReviewerPattern(BaseModel):
    reviewer_name: str
    review_count: int
    average_rating: float
    rating_variance: float
    suspicion_score: float
    flags: List[str]


class RatingDistribution(BaseModel):
    one_star: int
    two_star: int
    three_star: int
    four_star: int
    five_star: int
    total: int
    polarization_score: float  # 0-1, higher means more polarized


class BehaviorResponse(BaseModel):
    success: bool
    total_reviews: int
    temporal_patterns: List[TemporalPattern]
    reviewer_patterns: List[ReviewerPattern]
    rating_distribution: RatingDistribution
    aggregate_metrics: Dict[str, Any]
    timestamp: str