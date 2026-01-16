"""
Rating distribution analysis
"""
from typing import List
from collections import Counter

from models import Review, RatingDistribution
from config import settings


class RatingAnalyzer:
    """Analyze rating distribution patterns"""
    
    def analyze(self, reviews: List[Review]) -> RatingDistribution:
        """
        Analyze rating distribution
        Detect polarization (many 5-star and 1-star, few middle)
        
        Args:
            reviews: List of reviews to analyze
        
        Returns:
            RatingDistribution object with polarization score
        """
        if not reviews:
            return RatingDistribution(
                one_star=0, 
                two_star=0, 
                three_star=0, 
                four_star=0, 
                five_star=0, 
                total=0,
                polarization_score=0.0
            )
        
        # Count ratings
        rating_counts = Counter()
        for review in reviews:
            rating_int = int(round(review.rating))
            rating_counts[rating_int] += 1
        
        total = len(reviews)
        
        # Calculate polarization
        # High polarization = many 5-star and 1-star, few 2-4 star
        extreme_count = rating_counts[1] + rating_counts[5]
        middle_count = rating_counts[2] + rating_counts[3] + rating_counts[4]
        
        if total > 0:
            extreme_ratio = extreme_count / total
            polarization = extreme_ratio if extreme_ratio > settings.POLARIZATION_THRESHOLD else 0.0
        else:
            polarization = 0.0
        
        return RatingDistribution(
            one_star=rating_counts[1],
            two_star=rating_counts[2],
            three_star=rating_counts[3],
            four_star=rating_counts[4],
            five_star=rating_counts[5],
            total=total,
            polarization_score=round(polarization, 2)
        )