"""
ML-based sentiment analysis using VADER and TextBlob
"""
from typing import Tuple
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

from config import settings
from preprocessor import TextPreprocessor

# Download VADER lexicon
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


class MLSentimentAnalyzer:
    """ML-based sentiment analysis using VADER and TextBlob"""
    
    def __init__(self):
        # VADER for social media style text
        self.vader = SentimentIntensityAnalyzer()
        self.preprocessor = TextPreprocessor()
    
    def analyze(self, text: str) -> Tuple[float, str, float]:
        """
        Analyze sentiment using multiple methods
        
        Args:
            text: Review text to analyze
        
        Returns:
            Tuple of (score, label, confidence)
            - score: -1 to 1 (negative to positive)
            - label: 'positive', 'negative', or 'neutral'
            - confidence: 0 to 1 (agreement between methods)
        """
        if not text or len(text.strip()) < 5:
            return 0.0, 'neutral', 0.5
        
        # VADER analysis (better for informal text)
        vader_scores = self.vader.polarity_scores(text)
        vader_compound = vader_scores['compound']  # -1 to 1
        
        # TextBlob analysis (better for formal text)
        try:
            blob = TextBlob(text)
            textblob_polarity = blob.sentiment.polarity  # -1 to 1
        except:
            textblob_polarity = 0.0
        
        # Ensemble: weighted average
        score = (vader_compound * settings.VADER_WEIGHT + 
                textblob_polarity * settings.TEXTBLOB_WEIGHT)
        
        # Calculate confidence based on agreement
        agreement = 1 - abs(vader_compound - textblob_polarity) / 2
        confidence = min(0.95, max(0.5, agreement))
        
        # Determine label
        if score > settings.POSITIVE_THRESHOLD:
            label = 'positive'
        elif score < settings.NEGATIVE_THRESHOLD:
            label = 'negative'
        else:
            label = 'neutral'
        
        return round(score, 3), label, round(confidence, 3)
    
    def get_subjectivity(self, text: str) -> float:
        """
        Measure text subjectivity
        
        Args:
            text: Review text to analyze
        
        Returns:
            Score from 0 (objective) to 1 (subjective)
        """
        try:
            blob = TextBlob(text)
            return round(blob.sentiment.subjectivity, 3)
        except:
            return 0.5