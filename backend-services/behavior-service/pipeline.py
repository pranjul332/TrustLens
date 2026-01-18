"""
Main behavioral analysis pipeline
"""
from typing import List, Dict, Any
from datetime import datetime
import logging

from models import (
    Review, 
    TemporalPattern, 
    ReviewerPattern, 
    RatingDistribution,
    BehaviorResponse
)
from analyzers import TemporalAnalyzer, ReviewerAnalyzer, RatingAnalyzer
from config import settings

logger = logging.getLogger(__name__)


class BehaviorPipeline:
    """Main behavioral analysis pipeline"""
    
    def __init__(self):
        self.temporal_analyzer = TemporalAnalyzer()
        self.reviewer_analyzer = ReviewerAnalyzer()
        self.rating_analyzer = RatingAnalyzer()
    
    def analyze_reviews(self, reviews: List[Review]) -> BehaviorResponse:
        """
        Run complete behavioral analysis
        
        Args:
            reviews: List of reviews to analyze
        
        Returns:
            BehaviorResponse with all patterns and metrics
        """
        logger.info(f"Analyzing behavior patterns for {len(reviews)} reviews...")
        
        # Temporal patterns
        temporal_patterns = self.temporal_analyzer.analyze(reviews)
        
        # Reviewer patterns
        reviewer_patterns = self.reviewer_analyzer.analyze(reviews)
        
        # Rating distribution
        rating_dist = self.rating_analyzer.analyze(reviews)
        
        # Calculate aggregate metrics
        aggregate = self._calculate_aggregates(
            reviews, 
            temporal_patterns, 
            reviewer_patterns,
            rating_dist
        )
        
        logger.info(
            f"Behavior analysis complete. Found {len(temporal_patterns)} temporal patterns, "
            f"{len(reviewer_patterns)} reviewer patterns"
        )
        
        return BehaviorResponse(
            success=True,
            total_reviews=len(reviews),
            temporal_patterns=temporal_patterns,
            reviewer_patterns=reviewer_patterns,
            rating_distribution=rating_dist,
            aggregate_metrics=aggregate,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def _calculate_aggregates(
        self,
        reviews: List[Review],
        temporal_patterns: List[TemporalPattern],
        reviewer_patterns: List[ReviewerPattern],
        rating_dist: RatingDistribution
    ) -> Dict[str, Any]:
        """
        Calculate aggregate behavioral metrics
        
        Args:
            reviews: List of reviews
            temporal_patterns: Detected temporal patterns
            reviewer_patterns: Detected reviewer patterns
            rating_dist: Rating distribution
        
        Returns:
            Dictionary of aggregate metrics
        """
        
        # Temporal suspicion
        temporal_suspicion = 0.0
        if temporal_patterns:
            temporal_suspicion = sum(p.suspicion_score for p in temporal_patterns) / len(temporal_patterns)
        
        # Reviewer suspicion
        reviewer_suspicion = 0.0
        if reviewer_patterns:
            reviewer_suspicion = sum(p.suspicion_score for p in reviewer_patterns) / len(reviewer_patterns)
        
        # Rating suspicion (based on polarization and 5-star concentration)
        rating_suspicion = 0.0
        if rating_dist.total > 0:
            five_star_ratio = rating_dist.five_star / rating_dist.total
            # High 5-star concentration is suspicious
            if five_star_ratio > settings.HIGH_FIVE_STAR_THRESHOLD:
                rating_suspicion = min(1.0, five_star_ratio)
            
            # Add polarization
            rating_suspicion = max(rating_suspicion, rating_dist.polarization_score)
        
        # Overall behavior score (0-100)
        behavior_score = (
            temporal_suspicion * settings.TEMPORAL_WEIGHT +
            reviewer_suspicion * settings.REVIEWER_WEIGHT +
            rating_suspicion * settings.RATING_WEIGHT
        ) * 100
        
        # Verification rate
        verified_count = sum(1 for r in reviews if r.verified_purchase)
        verification_rate = (verified_count / len(reviews) * 100) if reviews else 0
        
        return {
            "temporal_suspicion": round(temporal_suspicion, 3),
            "reviewer_suspicion": round(reviewer_suspicion, 3),
            "rating_suspicion": round(rating_suspicion, 3),
            "behavior_fake_score": round(behavior_score, 2),  # 0-100 scale
            "has_burst_pattern": any(p.pattern_type == "burst" for p in temporal_patterns),
            "has_rating_spike": any(p.pattern_type == "rating_spike" for p in temporal_patterns),
            "has_recency_bias": any(p.pattern_type == "recency_bias" for p in temporal_patterns),
            "duplicate_reviewers_count": sum(1 for p in reviewer_patterns if p.review_count > 1),
            "verification_rate": round(verification_rate, 2),
            "polarization_detected": rating_dist.polarization_score > 0.5,
            "five_star_concentration": round((rating_dist.five_star / rating_dist.total * 100) if rating_dist.total > 0 else 0, 2)
        }