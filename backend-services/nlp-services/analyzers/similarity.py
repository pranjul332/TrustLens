"""
ML-based similarity detection using TF-IDF and cosine similarity
"""
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize

from models import Review, SimilarityCluster
from config import settings
from preprocessor import TextPreprocessor


class MLSimilarityDetector:
    """ML-based similarity detection using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TfidfVectorizer(
            max_features=settings.TFIDF_MAX_FEATURES,
            ngram_range=(settings.TFIDF_NGRAM_MIN, settings.TFIDF_NGRAM_MAX),
            min_df=settings.TFIDF_MIN_DF
        )
    
    def find_similar_reviews(
        self, 
        reviews: List[Review], 
        threshold: float = None
    ) -> List[SimilarityCluster]:
        """
        Find similar reviews using TF-IDF and cosine similarity
        
        Args:
            reviews: List of reviews to analyze
            threshold: Similarity threshold (default from config)
        
        Returns:
            List of similarity clusters
        """
        if threshold is None:
            threshold = settings.SIMILARITY_THRESHOLD
        
        if len(reviews) < 2:
            return []
        
        # Extract texts
        texts = [self.preprocessor.clean_text(r.text) for r in reviews]
        
        # Create TF-IDF matrix
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
        except:
            # Fallback if TF-IDF fails
            return self._fallback_similarity(reviews, settings.JACCARD_THRESHOLD)
        
        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Find clusters
        clusters = []
        processed = set()
        
        for i in range(len(reviews)):
            if i in processed:
                continue
            
            # Find similar reviews
            similar_indices = np.where(similarity_matrix[i] >= threshold)[0]
            similar_indices = [idx for idx in similar_indices if idx != i and idx not in processed]
            
            if len(similar_indices) > 0:
                cluster_ids = [reviews[i].review_id] + [reviews[j].review_id for j in similar_indices]
                avg_similarity = np.mean([similarity_matrix[i][j] for j in similar_indices])
                
                clusters.append(SimilarityCluster(
                    cluster_id=len(clusters),
                    review_ids=cluster_ids,
                    similarity_score=round(float(avg_similarity), 3),
                    sample_text=reviews[i].text[:100] + "..."
                ))
                
                processed.add(i)
                processed.update(similar_indices)
        
        return clusters
    
    def _fallback_similarity(self, reviews: List[Review], threshold: float) -> List[SimilarityCluster]:
        """Fallback to Jaccard similarity if TF-IDF fails"""
        clusters = []
        processed = set()
        
        for i, review1 in enumerate(reviews):
            if review1.review_id in processed:
                continue
            
            similar_reviews = [review1.review_id]
            
            for j, review2 in enumerate(reviews[i+1:], start=i+1):
                if review2.review_id in processed:
                    continue
                
                similarity = self._jaccard_similarity(review1.text, review2.text)
                
                if similarity >= threshold:
                    similar_reviews.append(review2.review_id)
                    processed.add(review2.review_id)
            
            if len(similar_reviews) > 1:
                clusters.append(SimilarityCluster(
                    cluster_id=len(clusters),
                    review_ids=similar_reviews,
                    similarity_score=round(threshold, 2),
                    sample_text=review1.text[:100] + "..."
                ))
                processed.add(review1.review_id)
        
        return clusters
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity"""
        words1 = set(word_tokenize(text1.lower()))
        words2 = set(word_tokenize(text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0