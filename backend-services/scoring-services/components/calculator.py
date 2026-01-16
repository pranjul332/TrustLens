"""
Trust score calculation component
"""
from typing import Dict, Any, Tuple

from models import NLPResults, BehaviorResults, ProductMetadata, ScoreBreakdown
from config import settings


class TrustScoreCalculator:
    """Calculate final trust score from all signals"""
    
    def calculate(
        self,
        nlp_results: NLPResults,
        behavior_results: BehaviorResults,
        product_metadata: ProductMetadata
    ) -> Tuple[int, ScoreBreakdown, float]:
        """
        Calculate final trust score (0-100)
        Higher score = more trustworthy
        Lower score = more suspicious
        
        Args:
            nlp_results: NLP analysis results
            behavior_results: Behavior analysis results
            product_metadata: Product information
        
        Returns:
            Tuple of (trust_score, breakdown, confidence)
        """
        
        # Extract component scores
        nlp_fake_score = nlp_results.aggregate_metrics.get("nlp_fake_score", 0)
        behavior_fake_score = behavior_results.aggregate_metrics.get("behavior_fake_score", 0)
        
        # Calculate statistical anomaly score
        statistical_score = self._calculate_statistical_score(
            behavior_results.rating_distribution,
            product_metadata
        )
        
        # Combine scores (all are 0-100, higher = more fake)
        weighted_fake_score = (
            nlp_fake_score * settings.NLP_WEIGHT +
            behavior_fake_score * settings.BEHAVIOR_WEIGHT +
            statistical_score * settings.STATISTICAL_WEIGHT
        )
        
        # Convert to trust score (invert: 100 - fake_score)
        trust_score = max(0, min(100, 100 - weighted_fake_score))
        
        # Calculate breakdown
        breakdown = ScoreBreakdown(
            nlp_contribution=round(nlp_fake_score * settings.NLP_WEIGHT, 2),
            behavior_contribution=round(behavior_fake_score * settings.BEHAVIOR_WEIGHT, 2),
            statistical_contribution=round(statistical_score * settings.STATISTICAL_WEIGHT, 2),
            final_score=round(trust_score, 2)
        )
        
        # Calculate confidence based on sample size and consistency
        confidence = self._calculate_confidence(
            nlp_results,
            behavior_results,
            product_metadata
        )
        
        return int(trust_score), breakdown, confidence
    
    def _calculate_statistical_score(
        self,
        rating_dist: Dict[str, Any],
        metadata: ProductMetadata
    ) -> float:
        """
        Calculate statistical anomaly score (0-100)
        Higher = more suspicious
        
        Args:
            rating_dist: Rating distribution
            metadata: Product metadata
        
        Returns:
            Statistical anomaly score (0-100)
        """
        score = 0.0
        
        total = rating_dist.get("total", 0)
        if total == 0:
            return 0.0
        
        # Signal 1: Five-star concentration (natural products: 40-60%)
        five_star = rating_dist.get("five_star", 0)
        five_star_ratio = five_star / total
        
        if five_star_ratio > settings.FIVE_STAR_CRITICAL:
            score += 40  # Very suspicious
        elif five_star_ratio > settings.FIVE_STAR_WARNING:
            score += 25  # Suspicious
        elif five_star_ratio > settings.FIVE_STAR_NOTICE:
            score += 10  # Slightly suspicious
        
        # Signal 2: Polarization (J-curve distribution)
        polarization = rating_dist.get("polarization_score", 0)
        if polarization > settings.POLARIZATION_CRITICAL:
            score += 30
        elif polarization > settings.POLARIZATION_WARNING:
            score += 15
        
        # Signal 3: Unnatural distribution (bell curve expected)
        one_star = rating_dist.get("one_star", 0)
        two_star = rating_dist.get("two_star", 0)
        three_star = rating_dist.get("three_star", 0)
        four_star = rating_dist.get("four_star", 0)
        
        # Check if middle ratings are suspiciously low
        middle_ratio = (two_star + three_star + four_star) / total
        if middle_ratio < settings.MIDDLE_RATIO_THRESHOLD:
            score += 20
        
        # Signal 4: Sample size consideration
        # Very few reviews with all 5-star is suspicious
        if total < settings.SMALL_SAMPLE_SIZE and five_star_ratio > settings.SMALL_SAMPLE_FIVE_STAR:
            score += 20
        
        return min(100, score)
    
    def _calculate_confidence(
        self,
        nlp_results: NLPResults,
        behavior_results: BehaviorResults,
        metadata: ProductMetadata
    ) -> float:
        """
        Calculate confidence in the assessment (0-1)
        Higher = more confident in the trust score
        
        Args:
            nlp_results: NLP analysis results
            behavior_results: Behavior analysis results
            metadata: Product metadata
        
        Returns:
            Confidence score (0-1)
        """
        confidence = settings.BASE_CONFIDENCE
        
        # Factor 1: Sample size (more reviews = more confident)
        total_reviews = behavior_results.aggregate_metrics.get("total_reviews", 0)
        if total_reviews >= settings.LARGE_SAMPLE_SIZE:
            confidence += 0.2
        elif total_reviews >= settings.MEDIUM_SAMPLE_SIZE:
            confidence += 0.15
        elif total_reviews >= settings.SMALL_SAMPLE_SIZE_CONF:
            confidence += 0.1
        
        # Factor 2: Signal consistency (all signals agree)
        nlp_fake = nlp_results.aggregate_metrics.get("nlp_fake_score", 0)
        behavior_fake = behavior_results.aggregate_metrics.get("behavior_fake_score", 0)
        
        # Calculate agreement (inverse of difference)
        score_diff = abs(nlp_fake - behavior_fake)
        if score_diff < settings.STRONG_AGREEMENT_THRESHOLD:
            confidence += 0.2  # Strong agreement
        elif score_diff < settings.MODERATE_AGREEMENT_THRESHOLD:
            confidence += 0.1  # Moderate agreement
        
        # Factor 3: Verification rate (more verified = more confident)
        verification_rate = behavior_results.aggregate_metrics.get("verification_rate", 0)
        if verification_rate > settings.HIGH_VERIFICATION_RATE:
            confidence += 0.1
        
        return min(1.0, round(confidence, 2))