"""
ML-powered NLP analysis pipeline
"""
from typing import List, Dict, Any
from datetime import datetime
from collections import Counter
import logging
import pandas as pd

from models import Review, ReviewAnalysis, SimilarityCluster, NLPResponse
from analyzers import (
    SentimentAnalyzer,
    FakeReviewDetector,
    TextQualityAnalyzer,
    PromotionalScorer,
    SimilarityDetector
)
from config import settings
from preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)


class NLPPipeline:
    """ML-powered NLP analysis pipeline"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.fake_detector = FakeReviewDetector()
        self.quality_analyzer = TextQualityAnalyzer()
        self.similarity_detector = SimilarityDetector()
        self.promo_scorer = PromotionalScorer()  # Rule-based (no ML version)
        self.preprocessor = TextPreprocessor()
    
    def analyze_reviews(self, reviews: List[Review]) -> NLPResponse:
        """
        Run complete ML-based NLP analysis
        
        Args:
            reviews: List of reviews to analyze
        
        Returns:
            NLPResponse with all analyses and metrics
        """
        logger.info(f"ML Analysis: Processing {len(reviews)} reviews...")
        
        analyses = []
        
        for review in reviews:
            # Sentiment analysis (ML)
            sentiment_score, sentiment_label, confidence = self.sentiment_analyzer.analyze(review.text)
            
            # Subjectivity (ML)
            subjectivity = self.sentiment_analyzer.get_subjectivity(review.text)
            
            # Fake detection (ML)
            fake_prob, flags = self.fake_detector.analyze(review, sentiment_score)
            
            # Text quality (ML)
            quality_metrics = self.quality_analyzer.analyze(review.text)
            
            # Promotional score (Rule-based - no ML version)
            promo_score = self.promo_scorer.analyze(review.text)
            
            analyses.append(ReviewAnalysis(
                review_id=review.review_id,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                sentiment_confidence=confidence,
                fake_probability=fake_prob,
                flags=flags,
                text_quality_score=quality_metrics['overall'],
                promotional_score=promo_score,
                readability_score=quality_metrics['readability'],
                subjectivity_score=subjectivity,
                lexical_diversity=quality_metrics['lexical_diversity']
            ))
        
        # Similarity detection using ML (TF-IDF)
        similarity_clusters = self.similarity_detector.find_similar_reviews(
            reviews, 
            threshold=settings.SIMILARITY_THRESHOLD
        )
        
        # Calculate aggregates
        aggregate = self._calculate_aggregates(analyses, similarity_clusters)
        
        logger.info(
            f"ML Analysis complete. Avg fake score: {aggregate.get('average_fake_probability', 0):.3f}"
        )
        
        return NLPResponse(
            success=True,
            total_reviews=len(reviews),
            analyses=analyses,
            similarity_clusters=similarity_clusters,
            aggregate_metrics=aggregate,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def _calculate_aggregates(
        self, 
        analyses: List[ReviewAnalysis], 
        clusters: List[SimilarityCluster]
    ) -> Dict[str, Any]:
        """
        Calculate aggregate statistics using pandas
        
        Args:
            analyses: List of individual review analyses
            clusters: List of similarity clusters
        
        Returns:
            Dictionary of aggregate metrics
        """
        if not analyses:
            return {}
        
        # Create DataFrame for easy analysis
        df = pd.DataFrame([{
            'fake_probability': a.fake_probability,
            'sentiment_score': a.sentiment_score,
            'sentiment_label': a.sentiment_label,
            'quality_score': a.text_quality_score,
            'promotional_score': a.promotional_score,
            'confidence': a.sentiment_confidence,
            'readability': a.readability_score,
            'subjectivity': a.subjectivity_score,
            'lexical_diversity': a.lexical_diversity,
            'flag_count': len(a.flags)
        } for a in analyses])
        
        # Sentiment distribution
        sentiment_dist = df['sentiment_label'].value_counts().to_dict()
        
        # Collect all flags
        all_flags = []
        for a in analyses:
            all_flags.extend(a.flags)
        flag_counts = Counter(all_flags).most_common(10)
        
        # High-risk reviews
        high_risk_count = len(df[df['fake_probability'] > settings.HIGH_RISK_THRESHOLD])
        
        # Duplicate percentage
        duplicate_count = sum(len(c.review_ids) for c in clusters)
        duplicate_percentage = (duplicate_count / len(analyses) * 100) if analyses else 0
        
        return {
            "average_fake_probability": round(float(df['fake_probability'].mean()), 3),
            "fake_probability_std": round(float(df['fake_probability'].std()), 3),
            "average_sentiment": round(float(df['sentiment_score'].mean()), 3),
            "sentiment_std": round(float(df['sentiment_score'].std()), 3),
            "average_confidence": round(float(df['confidence'].mean()), 3),
            "average_text_quality": round(float(df['quality_score'].mean()), 3),
            "average_readability": round(float(df['readability'].mean()), 3),
            "average_subjectivity": round(float(df['subjectivity'].mean()), 3),
            "average_lexical_diversity": round(float(df['lexical_diversity'].mean()), 3),
            "average_promotional_score": round(float(df['promotional_score'].mean()), 3),
            "sentiment_distribution": sentiment_dist,
            "high_risk_reviews_count": int(high_risk_count),
            "high_risk_percentage": round(float(high_risk_count / len(analyses) * 100), 2),
            "similarity_clusters_count": len(clusters),
            "duplicate_reviews_percentage": round(duplicate_percentage, 2),
            "common_flags": dict(flag_counts),
            "nlp_fake_score": round(float(df['fake_probability'].mean() * 100), 2),
            "quality_metrics": {
                "high_quality_count": int(len(df[df['quality_score'] > 0.7])),
                "low_quality_count": int(len(df[df['quality_score'] < 0.3])),
                "high_subjectivity_count": int(len(df[df['subjectivity'] > 0.7]))
            }
        }