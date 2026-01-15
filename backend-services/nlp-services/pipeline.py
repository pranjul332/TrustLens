"""
Main NLP analysis pipeline
"""
from typing import List, Dict, Any
from datetime import datetime
from collections import Counter
import logging

from models import Review, ReviewAnalysis, SimilarityCluster, NLPResponse
from analyzers import (
    SentimentAnalyzer,
    FakeReviewDetector,
    TextQualityAnalyzer,
    PromotionalScorer,
    SimilarityDetector
)
from config import settings

logger = logging.getLogger(__name__)


class NLPPipeline:
    """Main NLP analysis pipeline"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.fake_detector = FakeReviewDetector()
        self.quality_analyzer = TextQualityAnalyzer()
        self.promo_scorer = PromotionalScorer()
        self.similarity_detector = SimilarityDetector()
    
    def analyze_reviews(self, reviews: List[Review]) -> NLPResponse:
        """
        Run complete NLP analysis on reviews
        
        Args:
            reviews: List of reviews to analyze
        
        Returns:
            NLPResponse with all analyses and metrics
        """
        logger.info(f"Analyzing {len(reviews)} reviews...")
        
        analyses = []
        
        # Analyze each review
        for review in reviews:
            # Sentiment analysis
            sentiment_score, sentiment_label = self.sentiment_analyzer.analyze(review.text)
            
            # Fake detection
            fake_prob, flags = self.fake_detector.analyze(review)
            
            # Text quality
            quality_score = self.quality_analyzer.analyze(review.text)
            
            # Promotional score
            promo_score = self.promo_scorer.analyze(review.text)
            
            analyses.append(ReviewAnalysis(
                review_id=review.review_id,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                fake_probability=fake_prob,
                flags=flags,
                text_quality_score=quality_score,
                promotional_score=promo_score
            ))
        
        # Similarity detection
        similarity_clusters = self.similarity_detector.find_similar_reviews(
            reviews, 
            threshold=settings.SIMILARITY_THRESHOLD
        )
        
        # Calculate aggregate metrics
        aggregate = self._calculate_aggregates(analyses, similarity_clusters)
        
        logger.info(f"Analysis complete. Found {len(similarity_clusters)} similarity clusters")
        
        return NLPResponse(
            success=True,
            total_reviews=len(reviews),
            analyses=analyses,
            similarity_clusters=similarity_clusters,
            aggregate_metrics=aggregate,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def _calculate_aggregates(
        self, 
        analyses: List[ReviewAnalysis],
        clusters: List[SimilarityCluster]
    ) -> Dict[str, Any]:
        """
        Calculate aggregate statistics
        
        Args:
            analyses: List of individual review analyses
            clusters: List of similarity clusters
        
        Returns:
            Dictionary of aggregate metrics
        """
        if not analyses:
            return {}
        
        # Average scores
        avg_fake_prob = sum(a.fake_probability for a in analyses) / len(analyses)
        avg_quality = sum(a.text_quality_score for a in analyses) / len(analyses)
        avg_promo = sum(a.promotional_score for a in analyses) / len(analyses)
        avg_sentiment = sum(a.sentiment_score for a in analyses) / len(analyses)
        
        # Sentiment distribution
        sentiment_dist = Counter(a.sentiment_label for a in analyses)
        
        # Most common flags
        all_flags = []
        for a in analyses:
            all_flags.extend(a.flags)
        flag_counts = Counter(all_flags).most_common(10)
        
        # High-risk reviews (fake_probability > threshold)
        high_risk_count = sum(
            1 for a in analyses 
            if a.fake_probability > settings.HIGH_RISK_THRESHOLD
        )
        
        # Duplicate review percentage
        duplicate_count = sum(len(c.review_ids) for c in clusters)
        duplicate_percentage = (duplicate_count / len(analyses) * 100) if analyses else 0
        
        return {
            "average_fake_probability": round(avg_fake_prob, 3),
            "average_text_quality": round(avg_quality, 3),
            "average_promotional_score": round(avg_promo, 3),
            "average_sentiment": round(avg_sentiment, 3),
            "sentiment_distribution": dict(sentiment_dist),
            "high_risk_reviews_count": high_risk_count,
            "high_risk_percentage": round(high_risk_count / len(analyses) * 100, 2),
            "similarity_clusters_count": len(clusters),
            "duplicate_reviews_percentage": round(duplicate_percentage, 2),
            "common_flags": dict(flag_counts),
            "nlp_fake_score": round(avg_fake_prob * 100, 2)  # 0-100 scale
        }