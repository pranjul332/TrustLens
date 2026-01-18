"""
ML-based fake review detection with multi-feature analysis
"""
import re
from typing import List, Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer

from models import Review
from config import settings
from preprocessor import TextPreprocessor


class MLFakeReviewDetector:
    """Machine learning-based fake review detection"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.tfidf = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
        self.feature_weights = settings.FEATURE_WEIGHTS
        
    def analyze(self, review: Review, sentiment_score: float) -> Tuple[float, List[str]]:
        """
        ML-based fake review detection
        
        Args:
            review: Review object to analyze
            sentiment_score: Sentiment score from sentiment analyzer
        
        Returns:
            Tuple of (probability, flags)
            - probability: 0 to 1 (0 = genuine, 1 = definitely fake)
            - flags: List of detected issues
        """
        text = (review.text or '') + ' ' + (review.title or '')
        features = self.preprocessor.extract_features(text)
        
        flags = []
        scores = {}
        
        # 1. Text-based features
        text_score = self._analyze_text_features(features, flags)
        scores['text_features'] = text_score
        
        # 2. Promotional language detection
        promo_score = self._detect_promotional(text, flags)
        scores['promotional_score'] = promo_score
        
        # 3. Generic/template detection
        generic_score = self._detect_generic(text, flags)
        scores['generic_score'] = generic_score
        
        # 4. Quality indicators
        quality_score = self._assess_quality(features, flags)
        scores['quality_score'] = quality_score
        
        # 5. Sentiment-rating alignment
        mismatch_score = self._check_sentiment_rating_alignment(
            review.rating, sentiment_score, flags
        )
        scores['sentiment_rating_mismatch'] = mismatch_score
        
        # 6. Spam indicators
        spam_score = self._detect_spam(text, flags)
        scores['spam_indicators'] = spam_score
        
        # Weighted ensemble
        fake_probability = sum(
            scores.get(key, 0) * weight 
            for key, weight in self.feature_weights.items()
        )
        
        # Normalize to 0-1
        fake_probability = max(0.0, min(1.0, fake_probability))
        
        return round(fake_probability, 3), flags
    
    def _analyze_text_features(self, features: Dict[str, float], flags: List[str]) -> float:
        """Analyze structural text features"""
        score = 0.0
        
        # Very short reviews
        if features['word_count'] < settings.SHORT_REVIEW_LENGTH:
            flags.append('very_short')
            score += 0.4
        elif features['word_count'] < 20:
            score += 0.2
        
        # Excessive caps
        if features['caps_ratio'] > settings.MAX_CAPS_RATIO:
            flags.append('excessive_caps')
            score += 0.3
        
        # Excessive punctuation
        if features['exclamation_count'] > settings.MAX_EXCLAMATION_COUNT:
            flags.append('excessive_exclamation')
            score += 0.2
        
        # Low lexical diversity (repetitive)
        if (features['unique_word_ratio'] < settings.MIN_LEXICAL_DIVERSITY and 
            features['word_count'] > 20):
            flags.append('low_lexical_diversity')
            score += 0.3
        
        return min(1.0, score)
    
    def _detect_promotional(self, text: str, flags: List[str]) -> float:
        """Detect promotional language using NLP"""
        text_lower = text.lower()
        
        count = sum(1 for phrase in settings.PROMOTIONAL_PHRASES if phrase in text_lower)
        
        if count > 0:
            flags.append(f'promotional_language_detected')
        
        # Normalize
        score = min(1.0, count * 0.3)
        return score
    
    def _detect_generic(self, text: str, flags: List[str]) -> float:
        """Detect generic/template reviews"""
        text_lower = text.lower()
        
        count = sum(1 for template in settings.GENERIC_TEMPLATES if template in text_lower)
        
        if count >= 2:
            flags.append('generic_template')
        
        score = min(1.0, count * 0.25)
        return score
    
    def _assess_quality(self, features: Dict[str, float], flags: List[str]) -> float:
        """Assess text quality (higher quality = lower fake score)"""
        quality = 0.0
        
        # Good indicators
        if settings.IDEAL_MIN_LENGTH <= features['word_count'] <= settings.IDEAL_MAX_LENGTH:
            quality += 0.3
        
        if features['sentence_count'] >= 3:
            quality += 0.3
        
        if features['unique_word_ratio'] > 0.6:
            quality += 0.2
        
        if 4 <= features['avg_word_length'] <= 7:
            quality += 0.2
        
        return min(1.0, quality)
    
    def _check_sentiment_rating_alignment(
        self, rating: float, sentiment_score: float, flags: List[str]
    ) -> float:
        """Check if sentiment matches rating"""
        # Expected sentiment for rating
        if rating >= 4:
            expected_sentiment = 0.5  # positive
        elif rating <= 2:
            expected_sentiment = -0.5  # negative
        else:
            expected_sentiment = 0.0  # neutral
        
        # Calculate mismatch
        mismatch = abs(expected_sentiment - sentiment_score)
        
        if mismatch > 0.7:
            flags.append('sentiment_rating_mismatch')
            return 0.8
        elif mismatch > 0.5:
            return 0.4
        
        return 0.0
    
    def _detect_spam(self, text: str, flags: List[str]) -> float:
        """Detect spam patterns"""
        text_lower = text.lower()
        
        for pattern in settings.SPAM_PATTERNS:
            if re.search(pattern, text_lower):
                flags.append('spam_pattern_detected')
                return 0.9
        
        return 0.0