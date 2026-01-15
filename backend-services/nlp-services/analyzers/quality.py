"""
Text quality analysis
"""
import re

from config import settings


class TextQualityAnalyzer:
    """Analyze text quality and informational content"""
    
    def analyze(self, text: str) -> float:
        """
        Measure text quality
        
        Args:
            text: Review text to analyze
        
        Returns:
            Score from 0 to 1 (0 = poor, 1 = high quality)
        """
        if not text or len(text.strip()) < settings.MIN_TEXT_LENGTH:
            return 0.0
        
        score = 0.0
        
        # Length check (ideal: 50-500 characters)
        length = len(text.strip())
        if settings.IDEAL_MIN_LENGTH <= length <= settings.IDEAL_MAX_LENGTH:
            score += 0.3
        elif (settings.IDEAL_MIN_LENGTH // 2 <= length < settings.IDEAL_MIN_LENGTH or 
              settings.IDEAL_MAX_LENGTH < length <= settings.MAX_ACCEPTABLE_LENGTH):
            score += 0.15
        
        # Sentence structure (has periods)
        sentence_count = len(re.split(r'[.!?]+', text))
        if sentence_count >= 2:
            score += 0.2
        
        # Vocabulary diversity
        words = re.findall(r'\b\w+\b', text.lower())
        if words:
            unique_ratio = len(set(words)) / len(words)
            score += unique_ratio * 0.3
        
        # Grammar indicators (basic)
        has_proper_grammar = any(char in text for char in ['.', ',', '!', '?'])
        if has_proper_grammar:
            score += 0.2
        
        return min(1.0, round(score, 3))