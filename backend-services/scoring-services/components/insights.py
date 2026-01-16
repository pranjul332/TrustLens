"""
Insight generation component
"""
from typing import List

from models import NLPResults, BehaviorResults, Insight
from config import settings


class InsightGenerator:
    """Generate human-readable insights from analysis results"""
    
    def generate(
        self,
        nlp_results: NLPResults,
        behavior_results: BehaviorResults,
        trust_score: int
    ) -> List[Insight]:
        """
        Generate prioritized list of insights
        
        Args:
            nlp_results: NLP analysis results
            behavior_results: Behavior analysis results
            trust_score: Calculated trust score
        
        Returns:
            List of insights sorted by severity
        """
        insights = []
        
        # NLP-based insights
        insights.extend(self._generate_nlp_insights(nlp_results))
        
        # Behavior-based insights
        insights.extend(self._generate_behavior_insights(behavior_results))
        
        # Statistical insights
        insights.extend(self._generate_statistical_insights(behavior_results))
        
        # Sort by severity (high -> medium -> low)
        severity_order = {"high": 0, "medium": 1, "low": 2}
        insights.sort(key=lambda x: severity_order.get(x.severity, 3))
        
        # Return top insights
        return insights[:settings.MAX_INSIGHTS]
    
    def _generate_nlp_insights(self, nlp_results: NLPResults) -> List[Insight]:
        """Generate insights from NLP analysis"""
        insights = []
        metrics = nlp_results.aggregate_metrics
        
        # High fake probability
        avg_fake_prob = metrics.get("average_fake_probability", 0)
        if avg_fake_prob > settings.HIGH_FAKE_PROB:
            insights.append(Insight(
                category="red_flag",
                severity="high",
                title="High Fake Review Probability",
                description=f"{avg_fake_prob*100:.0f}% average fake probability detected across reviews",
                evidence=f"NLP analysis flagged {metrics.get('high_risk_reviews_count', 0)} high-risk reviews"
            ))
        elif avg_fake_prob > settings.MEDIUM_FAKE_PROB:
            insights.append(Insight(
                category="warning",
                severity="medium",
                title="Moderate Fake Review Risk",
                description=f"{avg_fake_prob*100:.0f}% average fake probability detected",
                evidence="Multiple promotional patterns and template-style reviews found"
            ))
        
        # Similarity clusters (duplicates)
        cluster_count = metrics.get("similarity_clusters_count", 0)
        duplicate_pct = metrics.get("duplicate_reviews_percentage", 0)
        if cluster_count > 0 and duplicate_pct > settings.DUPLICATE_THRESHOLD:
            insights.append(Insight(
                category="red_flag",
                severity="high",
                title="Duplicate Reviews Detected",
                description=f"{duplicate_pct:.1f}% of reviews are near-duplicates",
                evidence=f"Found {cluster_count} clusters of similar reviews"
            ))
        
        # Common flags
        common_flags = metrics.get("common_flags", {})
        if common_flags:
            top_flag = max(common_flags, key=common_flags.get)
            count = common_flags[top_flag]
            if count > 5:
                flag_name = top_flag.replace("_", " ").title()
                insights.append(Insight(
                    category="warning",
                    severity="medium",
                    title=f"Repeated Pattern: {flag_name}",
                    description=f"Detected {count} times across reviews",
                    evidence="Consistent pattern suggests coordinated activity"
                ))
        
        # Sentiment mismatch
        sentiment_dist = metrics.get("sentiment_distribution", {})
        positive_count = sentiment_dist.get("positive", 0)
        total_reviews = sum(sentiment_dist.values()) if sentiment_dist else 0
        if total_reviews > 0 and positive_count / total_reviews > settings.UNUSUALLY_POSITIVE:
            insights.append(Insight(
                category="warning",
                severity="low",
                title="Unusually Positive Sentiment",
                description=f"{positive_count/total_reviews*100:.0f}% positive reviews (natural range: 60-75%)",
                evidence="May indicate selection bias or fake positive reviews"
            ))
        
        # Low text quality
        avg_quality = metrics.get("average_text_quality", 1.0)
        if avg_quality < settings.LOW_TEXT_QUALITY:
            insights.append(Insight(
                category="warning",
                severity="medium",
                title="Low Review Quality",
                description=f"Average text quality score: {avg_quality:.2f}/1.0",
                evidence="Many reviews lack detail or informational content"
            ))
        
        return insights
    
    def _generate_behavior_insights(self, behavior_results: BehaviorResults) -> List[Insight]:
        """Generate insights from behavioral analysis"""
        insights = []
        metrics = behavior_results.aggregate_metrics
        
        # Review burst
        if metrics.get("has_burst_pattern"):
            for pattern in behavior_results.temporal_patterns:
                if pattern.get("pattern_type") == "burst":
                    insights.append(Insight(
                        category="red_flag",
                        severity="high",
                        title="Review Burst Detected",
                        description=pattern.get("description", "Suspicious burst of reviews"),
                        evidence=f"Suspicion score: {pattern.get('suspicion_score', 0):.2f}"
                    ))
                    break
        
        # Rating spike
        if metrics.get("has_rating_spike"):
            insights.append(Insight(
                category="red_flag",
                severity="high",
                title="Sudden Rating Spike",
                description="Unusual sudden increase in average rating",
                evidence="May indicate coordinated fake positive reviews"
            ))
        
        # Recency bias
        if metrics.get("has_recency_bias"):
            insights.append(Insight(
                category="warning",
                severity="medium",
                title="Recency Bias Detected",
                description="Majority of reviews posted recently",
                evidence="Possible ongoing review campaign"
            ))
        
        # Low verification rate
        verification_rate = metrics.get("verification_rate", 100)
        if verification_rate < settings.VERY_LOW_VERIFICATION:
            insights.append(Insight(
                category="red_flag",
                severity="high",
                title="Very Low Verification Rate",
                description=f"Only {verification_rate:.0f}% verified purchases",
                evidence="Most reviews not from verified buyers"
            ))
        elif verification_rate < settings.LOW_VERIFICATION:
            insights.append(Insight(
                category="warning",
                severity="medium",
                title="Low Verification Rate",
                description=f"{verification_rate:.0f}% verified purchases (typical: 70-80%)",
                evidence="Below-average verification ratio"
            ))
        
        # Duplicate reviewers
        duplicate_count = metrics.get("duplicate_reviewers_count", 0)
        if duplicate_count > 0:
            insights.append(Insight(
                category="warning",
                severity="medium",
                title="Duplicate Reviewers Found",
                description=f"{duplicate_count} reviewers posted multiple times",
                evidence="Same users leaving multiple reviews"
            ))
        
        # Polarization
        if metrics.get("polarization_detected"):
            insights.append(Insight(
                category="warning",
                severity="medium",
                title="Rating Polarization",
                description="Unnatural distribution with mostly 5⭐ and 1⭐ reviews",
                evidence="Typical products have bell curve distribution"
            ))
        
        return insights
    
    def _generate_statistical_insights(self, behavior_results: BehaviorResults) -> List[Insight]:
        """Generate insights from statistical analysis"""
        insights = []
        metrics = behavior_results.aggregate_metrics
        rating_dist = behavior_results.rating_distribution
        
        # Five-star concentration
        five_star_pct = metrics.get("five_star_concentration", 0)
        if five_star_pct > settings.EXTREME_FIVE_STAR:
            insights.append(Insight(
                category="red_flag",
                severity="high",
                title="Extreme Five-Star Concentration",
                description=f"{five_star_pct:.0f}% of reviews are 5-star",
                evidence="Natural products typically have 40-60% five-star reviews"
            ))
        elif five_star_pct > settings.HIGH_FIVE_STAR:
            insights.append(Insight(
                category="warning",
                severity="medium",
                title="High Five-Star Concentration",
                description=f"{five_star_pct:.0f}% five-star reviews (above typical range)",
                evidence="May indicate fake positive reviews"
            ))
        
        # Low sample size warning
        total = rating_dist.get("total", 0)
        if total < settings.SMALL_SAMPLE_SIZE and five_star_pct > 80:
            insights.append(Insight(
                category="warning",
                severity="low",
                title="Limited Sample Size",
                description=f"Analysis based on only {total} reviews",
                evidence="Small sample with high ratings may be misleading"
            ))
        
        return insights