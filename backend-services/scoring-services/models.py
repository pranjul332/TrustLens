"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class NLPResults(BaseModel):
    aggregate_metrics: Dict[str, Any]
    similarity_clusters: List[Dict[str, Any]] = []


class BehaviorResults(BaseModel):
    aggregate_metrics: Dict[str, Any]
    temporal_patterns: List[Dict[str, Any]] = []
    reviewer_patterns: List[Dict[str, Any]] = []
    rating_distribution: Dict[str, Any]


class ProductMetadata(BaseModel):
    product_name: str
    platform: str
    total_ratings: Optional[int] = None
    average_rating: Optional[float] = None
    rating_distribution: Optional[Dict[str, int]] = None


class ScoreRequest(BaseModel):
    nlp_results: NLPResults
    behavior_results: BehaviorResults
    product_metadata: ProductMetadata


class Insight(BaseModel):
    category: str  # red_flag, warning, positive
    severity: str  # high, medium, low
    title: str
    description: str
    evidence: Optional[str] = None


class ScoreBreakdown(BaseModel):
    nlp_contribution: float
    behavior_contribution: float
    statistical_contribution: float
    final_score: float


class ScoreResponse(BaseModel):
    success: bool
    trust_score: int  # 0-100 (100 = fully trustworthy)
    fake_reviews_percentage: float
    risk_level: str  # low, medium, high, critical
    score_breakdown: ScoreBreakdown
    key_insights: List[Insight]
    total_reviews_analyzed: int
    recommendation: str
    confidence: float  # 0-1 (confidence in the assessment)
    timestamp: str