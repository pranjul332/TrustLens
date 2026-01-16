"""
Main scoring pipeline orchestrator
"""
from datetime import datetime
import logging

from models import (
    NLPResults,
    BehaviorResults,
    ProductMetadata,
    ScoreResponse
)
from components import (
    TrustScoreCalculator,
    InsightGenerator,
    RecommendationEngine,
    RiskClassifier
)

logger = logging.getLogger(__name__)


class ScoringPipeline:
    """Main scoring pipeline orchestrator"""
    
    def __init__(self):
        self.calculator = TrustScoreCalculator()
        self.insight_generator = InsightGenerator()
        self.recommender = RecommendationEngine()
        self.risk_classifier = RiskClassifier()
    
    def generate_final_score(
        self,
        nlp_results: NLPResults,
        behavior_results: BehaviorResults,
        product_metadata: ProductMetadata
    ) -> ScoreResponse:
        """
        Generate comprehensive final score and report
        
        Args:
            nlp_results: NLP analysis results
            behavior_results: Behavior analysis results
            product_metadata: Product information
        
        Returns:
            Complete score response with insights
        """
        
        logger.info("Generating final trust score...")
        
        # Calculate trust score
        trust_score, breakdown, confidence = self.calculator.calculate(
            nlp_results,
            behavior_results,
            product_metadata
        )
        
        # Generate insights
        insights = self.insight_generator.generate(
            nlp_results,
            behavior_results,
            trust_score
        )
        
        # Classify risk
        risk_level = self.risk_classifier.classify(trust_score)
        
        # Generate recommendation
        recommendation = self.recommender.generate_recommendation(trust_score, risk_level)
        
        # Calculate fake review percentage
        fake_percentage = 100 - trust_score
        
        # Get total reviews analyzed
        total_reviews = behavior_results.aggregate_metrics.get("total_reviews", 0)
        
        logger.info(
            f"Final score generated: Trust={trust_score}, "
            f"Risk={risk_level}, Confidence={confidence}"
        )
        
        return ScoreResponse(
            success=True,
            trust_score=trust_score,
            fake_reviews_percentage=round(fake_percentage, 1),
            risk_level=risk_level,
            score_breakdown=breakdown,
            key_insights=insights,
            total_reviews_analyzed=total_reviews,
            recommendation=recommendation,
            confidence=confidence,
            timestamp=datetime.utcnow().isoformat()
        )