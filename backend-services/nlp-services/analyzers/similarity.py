"""
Review similarity and duplicate detection
"""
import re
from typing import List

from models import Review, SimilarityCluster
from config import settings


class SimilarityDetector:
    """Detect similar/duplicate reviews using text similarity"""
    
    def find_similar_reviews(
        self, 
        reviews: List[Review], 
        threshold: float = None
    ) -> List[SimilarityCluster]:
        """
        Find clusters of similar reviews
        
        Args:
            reviews: List of reviews to analyze
            threshold: Similarity threshold (default from config)
        
        Returns:
            List of clusters with similar reviews
        """
        if threshold is None:
            threshold = settings.SIMILARITY_THRESHOLD
        
        if len(reviews) < 2:
            return []
        
        clusters = []
        processed = set()
        
        for i, review1 in enumerate(reviews):
            if review1.review_id in processed:
                continue
            
            similar_reviews = [review1.review_id]
            
            for j, review2 in enumerate(reviews[i+1:], start=i+1):
                if review2.review_id in processed:
                    continue
                
                # Calculate similarity
                similarity = self._calculate_similarity(review1.text, review2.text)
                
                if similarity >= threshold:
                    similar_reviews.append(review2.review_id)
                    processed.add(review2.review_id)
            
            if len(similar_reviews) > 1:
                # Found a cluster
                clusters.append(SimilarityCluster(
                    cluster_id=len(clusters),
                    review_ids=similar_reviews,
                    similarity_score=round(threshold, 2),
                    sample_text=review1.text[:100] + "..."
                ))
                processed.add(review1.review_id)
        
        return clusters
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity using Jaccard similarity
        (Simple but effective for duplicate detection)
        
        Args:
            text1: First text to compare
            text2: Second text to compare
        
        Returns:
            Similarity score from 0 to 1
        """
        if not text1 or not text2:
            return 0.0
        
        # Tokenize
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard similarity: intersection / union
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0