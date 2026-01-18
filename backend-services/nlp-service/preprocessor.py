"""
Text preprocessing and feature extraction
"""
import re
import string
from typing import List, Dict
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class TextPreprocessor:
    """Advanced text preprocessing pipeline"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = nltk.WordNetLemmatizer() if hasattr(nltk, 'WordNetLemmatizer') else None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove phone numbers
        text = re.sub(r'\b\d{10,}\b', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str, remove_stopwords: bool = False) -> List[str]:
        """Tokenize text into words"""
        tokens = word_tokenize(text.lower())
        
        # Remove punctuation
        tokens = [w for w in tokens if w not in string.punctuation]
        
        if remove_stopwords:
            tokens = [w for w in tokens if w not in self.stop_words]
        
        return tokens
    
    def extract_features(self, text: str) -> Dict[str, float]:
        """Extract text features for ML models"""
        if not text:
            return self._empty_features()
        
        clean_text = self.clean_text(text)
        tokens = self.tokenize(clean_text)
        sentences = sent_tokenize(text)
        
        features = {
            'length': len(text),
            'word_count': len(tokens),
            'sentence_count': len(sentences),
            'avg_word_length': np.mean([len(w) for w in tokens]) if tokens else 0,
            'avg_sentence_length': len(tokens) / len(sentences) if sentences else 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'caps_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
            'digit_ratio': sum(1 for c in text if c.isdigit()) / len(text) if text else 0,
            'punctuation_ratio': sum(1 for c in text if c in string.punctuation) / len(text) if text else 0,
            'unique_word_ratio': len(set(tokens)) / len(tokens) if tokens else 0,
        }
        
        return features
    
    def _empty_features(self) -> Dict[str, float]:
        """Return empty feature set"""
        return {k: 0.0 for k in [
            'length', 'word_count', 'sentence_count', 'avg_word_length',
            'avg_sentence_length', 'exclamation_count', 'question_count',
            'caps_ratio', 'digit_ratio', 'punctuation_ratio', 'unique_word_ratio'
        ]}