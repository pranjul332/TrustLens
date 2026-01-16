"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class Review(BaseModel):
    review_id: str
    rating: float
    text: str
    title: Optional[str] = None


class AnalyzeRequest(BaseModel):
    reviews: List[Review]


class ReviewAnalysis(BaseModel):
    review_id: str
    sentiment_score: float  # -1 to 1
    sentiment_label: str  # positive, negative, neutral
    sentiment_confidence: float  # 0 to 1 (ML only)
    fake_probability: float  # 0 to 1
    flags: List[str]
    text_quality_score: float  # 0 to 1
    promotional_score: float  # 0 to 1
    readability_score: float  # 0 to 1 (ML only)
    subjectivity_score: float  # 0 to 1 (ML only)
    lexical_diversity: float  # 0 to 1 (ML only)


class SimilarityCluster(BaseModel):
    cluster_id: int
    review_ids: List[str]
    similarity_score: float
    sample_text: str


class NLPResponse(BaseModel):
    success: bool
    total_reviews: int
    analyses: List[ReviewAnalysis]
    similarity_clusters: List[SimilarityCluster]
    aggregate_metrics: Dict[str, Any]
    timestamp: str


class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    text: str
    sentiment_score: float
    sentiment_label: str
    confidence: Optional[float] = None
    subjectivity: Optional[float] = None