"""
Sentiment analysis component
"""
import re
from typing import Tuple

from config import settings


class SentimentAnalyzer:
    """Rule-based sentiment analyzer"""
    
    def __init__(self):
        self.positive_words = settings.POSITIVE_WORDS
        self.negative_words = settings.NEGATIVE_WORDS
        self.intensifiers = settings.INTENSIFIER_WORDS
    
    def analyze(self, text: str) -> Tuple[float, str]:
        """
        Analyze sentiment of text
        
        Args:
            text: Review text to analyze
        
        Returns:
            Tuple of (score, label)
            - score: -1 (very negative) to 1 (very positive)
            - label: 'positive', 'negative', or 'neutral'
        """
        if not text or len(text.strip()) < 5:
            return 0.0, 'neutral'
        
        # Clean and tokenize
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return 0.0, 'neutral'
        
        # Count positive and negative words
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        # Check for intensifiers (multiply impact)
        intensifier_multiplier = 1.0
        for word in words:
            if word in self.intensifiers:
                intensifier_multiplier += 0.2
        
        # Calculate score
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            return 0.0, 'neutral'
        
        # Weighted score
        score = (positive_count - negative_count) / len(words)
        score = score * intensifier_multiplier
        
        # Normalize to -1 to 1
        score = max(-1.0, min(1.0, score * 10))
        
        # Determine label
        if score > 0.2:
            label = 'positive'
        elif score < -0.2:
            label = 'negative'
        else:
            label = 'neutral'
        
        return round(score, 3), label