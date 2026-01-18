"""
ML-based text quality analysis
"""
from typing import Dict

from config import settings
from preprocessor import TextPreprocessor


class MLTextQualityAnalyzer:
    """ML-based text quality analysis"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Comprehensive quality analysis
        
        Args:
            text: Review text to analyze
        
        Returns:
            Dictionary with overall, readability, and lexical_diversity scores
        """
        if not text or len(text.strip()) < settings.MIN_TEXT_LENGTH:
            return {
                'overall': 0.0, 
                'readability': 0.0, 
                'lexical_diversity': 0.0
            }
        
        features = self.preprocessor.extract_features(text)
        
        # Readability score (Flesch-like)
        readability = self._calculate_readability(features)
        
        # Lexical diversity (unique words / total words)
        lexical_diversity = features['unique_word_ratio']
        
        # Overall quality score
        overall = (
            readability * settings.READABILITY_WEIGHT +
            lexical_diversity * settings.LEXICAL_DIVERSITY_WEIGHT +
            self._length_score(features['word_count']) * settings.LENGTH_WEIGHT
        )
        
        return {
            'overall': round(overall, 3),
            'readability': round(readability, 3),
            'lexical_diversity': round(lexical_diversity, 3)
        }
    
    def _calculate_readability(self, features: Dict[str, float]) -> float:
        """Calculate readability score (0-1)"""
        # Ideal: avg word length 4-7, avg sentence length 10-20
        word_score = 1 - abs(features['avg_word_length'] - settings.IDEAL_AVG_WORD_LENGTH) / settings.IDEAL_AVG_WORD_LENGTH
        sentence_score = 1 - abs(features['avg_sentence_length'] - settings.IDEAL_AVG_SENTENCE_LENGTH) / settings.IDEAL_AVG_SENTENCE_LENGTH
        
        return max(0, min(1, (word_score + sentence_score) / 2))
    
    def _length_score(self, word_count: int) -> float:
        """Score based on text length"""
        if settings.IDEAL_MIN_LENGTH <= word_count <= settings.IDEAL_MAX_LENGTH:
            return 1.0
        elif 30 <= word_count < settings.IDEAL_MIN_LENGTH or settings.IDEAL_MAX_LENGTH < word_count <= 300:
            return 0.7
        elif 20 <= word_count < 30 or 300 < word_count <= settings.MAX_ACCEPTABLE_LENGTH:
            return 0.5
        else:
            return 0.3