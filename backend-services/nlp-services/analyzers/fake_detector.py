"""
Fake review detection using NLP signals
"""
import re
from typing import List, Tuple
from collections import Counter

from models import Review
from config import settings
from analyzers.sentiment import SentimentAnalyzer


class FakeReviewDetector:
    """Detect fake/suspicious reviews using NLP signals"""
    
    def __init__(self):
        # Promotional phrases
        self.promotional_phrases = [
            'must buy', 'highly recommend', 'best buy', 'grab it', 
            'don\'t miss', 'amazing deal', 'worth every penny',
            'go for it', 'blindly buy', 'just buy it', 'buy now',
            'genuine product', 'original product', 'authentic',
            'value for money', 'paisa vasool', 'super product'
        ]
        
        # Generic/template phrases
        self.generic_phrases = [
            'nice product', 'good product', 'awesome product',
            'excellent product', 'great product', 'superb product',
            'amazing product', 'loved it', 'love it', 'like it'
        ]
        
        # Spam indicators
        self.spam_patterns = [
            r'\b\d{10}\b',  # Phone numbers
            r'whatsapp',
            r'contact.*\d',
            r'click.*link',
            r'visit.*website'
        ]
        
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def analyze(self, review: Review) -> Tuple[float, List[str]]:
        """
        Detect if review is likely fake
        
        Args:
            review: Review object to analyze
        
        Returns:
            Tuple of (probability, flags)
            - probability: 0 to 1 (0 = genuine, 1 = definitely fake)
            - flags: List of detected issues
        """
        text = (review.text or '') + ' ' + (review.title or '')
        text_lower = text.lower()
        
        flags = []
        score = 0.0
        
        # Check 1: Text length
        if len(text.strip()) < settings.SHORT_REVIEW_LENGTH:
            flags.append('very_short_review')
            score += 0.3
        
        # Check 2: Promotional language
        promo_count = sum(1 for phrase in self.promotional_phrases if phrase in text_lower)
        if promo_count > 0:
            flags.append(f'promotional_language_{promo_count}x')
            score += min(0.4, promo_count * 0.2)
        
        # Check 3: Generic phrases
        generic_count = sum(1 for phrase in self.generic_phrases if phrase in text_lower)
        if generic_count >= 2:
            flags.append('generic_template')
            score += 0.3
        
        # Check 4: Spam patterns
        for pattern in self.spam_patterns:
            if re.search(pattern, text_lower):
                flags.append('spam_pattern')
                score += 0.4
                break
        
        # Check 5: Rating-sentiment mismatch
        sentiment_score, _ = self.sentiment_analyzer.analyze(text)
        
        # If 5-star but negative sentiment
        if review.rating >= 4.5 and sentiment_score < -0.3:
            flags.append('rating_sentiment_mismatch')
            score += 0.4
        
        # If 1-star but positive sentiment
        if review.rating <= 2.0 and sentiment_score > 0.3:
            flags.append('rating_sentiment_mismatch')
            score += 0.4
        
        # Check 6: Excessive exclamation/caps
        exclamation_count = text.count('!')
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        if exclamation_count > settings.MAX_EXCLAMATION_COUNT:
            flags.append('excessive_exclamation')
            score += 0.2
        
        if caps_ratio > settings.MAX_CAPS_RATIO:
            flags.append('excessive_caps')
            score += 0.2
        
        # Check 7: Repetitive words
        words = re.findall(r'\b\w+\b', text_lower)
        if words:
            word_freq = Counter(words)
            most_common = word_freq.most_common(1)[0]
            if most_common[1] > settings.MAX_WORD_REPETITION:
                flags.append('repetitive_words')
                score += 0.2
        
        # Check 8: Too perfect (only superlatives)
        superlatives = ['best', 'perfect', 'excellent', 'amazing', 'awesome']
        if len(words) < 50 and sum(1 for word in words if word in superlatives) >= 3:
            flags.append('too_perfect')
            score += 0.3
        
        # Normalize score to 0-1
        score = min(1.0, score)
        
        return round(score, 3), flags