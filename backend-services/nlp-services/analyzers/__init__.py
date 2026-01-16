"""
NLP Analyzers package initialization
ML-based analyzers + rule-based promotional scorer
"""
# ML-based analyzers
from .sentiment import MLSentimentAnalyzer
from .fake_detector import MLFakeReviewDetector
from .quality import MLTextQualityAnalyzer
from .similarity import MLSimilarityDetector

# Rule-based (only for features without ML version)
from .promotional import PromotionalScorer

__all__ = [
    "MLSentimentAnalyzer",
    "MLFakeReviewDetector",
    "MLTextQualityAnalyzer",
    "MLSimilarityDetector",
    "PromotionalScorer"
]