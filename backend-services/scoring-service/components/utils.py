"""
Utility components for scoring
"""
from config import settings


class RecommendationEngine:
    """Generate purchase recommendations"""
    
    def generate_recommendation(self, trust_score: int, risk_level: str) -> str:
        """
        Generate user-friendly recommendation
        
        Args:
            trust_score: Trust score (0-100)
            risk_level: Risk level classification
        
        Returns:
            User-friendly recommendation string
        """
        if trust_score >= settings.TRUST_EXCELLENT:
            return "✅ RECOMMENDED: Reviews appear genuine. Safe to purchase based on review analysis."
        elif trust_score >= settings.TRUST_GOOD:
            return "⚠️ PROCEED WITH CAUTION: Some suspicious patterns detected. Research product further before buying."
        elif trust_score >= settings.TRUST_POOR:
            return "⚠️ NOT RECOMMENDED: Multiple red flags detected. Consider alternative products."
        else:
            return "🚫 AVOID: High likelihood of fake reviews. Do not trust the ratings."


class RiskClassifier:
    """Classify overall risk level"""
    
    def classify(self, trust_score: int) -> str:
        """
        Classify risk level based on trust score
        
        Args:
            trust_score: Trust score (0-100)
        
        Returns:
            Risk level (low/medium/high/critical)
        """
        if trust_score >= settings.TRUST_EXCELLENT:
            return "low"
        elif trust_score >= settings.TRUST_GOOD:
            return "medium"
        elif trust_score >= settings.TRUST_POOR:
            return "high"
        else:
            return "critical"