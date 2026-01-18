"""
Promotional content detection
"""
import re

from config import settings


class PromotionalScorer:
    """Detect promotional content"""
    
    def __init__(self):
        self.promotional_keywords = settings.PROMOTIONAL_KEYWORDS
    
    def analyze(self, text: str) -> float:
        """
        Score promotional intensity
        
        Args:
            text: Review text to analyze
        
        Returns:
            Score from 0 to 1 (0 = informative, 1 = highly promotional)
        """
        if not text:
            return 0.0
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return 0.0
        
        # Count promotional words
        promo_count = sum(1 for word in words if word in self.promotional_keywords)
        promo_ratio = promo_count / len(words)
        
        # Score based on ratio
        score = min(1.0, promo_ratio * 10)
        
        return round(score, 3)