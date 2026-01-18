"""
Reviewer behavior pattern detection
"""
from typing import List, Optional
from collections import defaultdict

from models import Review, ReviewerPattern
from config import settings


class ReviewerAnalyzer:
    """Analyze reviewer behavior patterns"""
    
    def analyze(self, reviews: List[Review]) -> List[ReviewerPattern]:
        """
        Detect suspicious reviewer patterns:
        - Same reviewer multiple times
        - Unverified purchases
        - Rating patterns
        
        Args:
            reviews: List of reviews to analyze
        
        Returns:
            List of reviewer patterns
        """
        patterns = []
        
        # Group by reviewer
        reviewer_groups = defaultdict(list)
        for review in reviews:
            if review.reviewer_name:
                reviewer_groups[review.reviewer_name].append(review)
        
        # Analyze each reviewer
        for reviewer_name, reviewer_reviews in reviewer_groups.items():
            if len(reviewer_reviews) > 1:  # Multiple reviews from same person
                pattern = self._analyze_reviewer(reviewer_name, reviewer_reviews)
                if pattern:
                    patterns.append(pattern)
        
        # Analyze unverified purchase ratio
        unverified_pattern = self._analyze_verification(reviews)
        if unverified_pattern:
            patterns.append(unverified_pattern)
        
        return patterns
    
    def _analyze_reviewer(
        self, 
        reviewer_name: str, 
        reviews: List[Review]
    ) -> Optional[ReviewerPattern]:
        """Analyze a single reviewer's behavior"""
        flags = []
        suspicion = 0.0
        
        # Multiple reviews from same person (suspicious)
        if len(reviews) > 1:
            flags.append(f"multiple_reviews_{len(reviews)}x")
            suspicion += min(0.5, len(reviews) * 0.2)
        
        # Calculate rating statistics
        ratings = [r.rating for r in reviews]
        avg_rating = sum(ratings) / len(ratings)
        
        # Rating variance
        variance = sum((r - avg_rating) ** 2 for r in ratings) / len(ratings)
        
        # All same rating (bot-like behavior)
        if variance == 0 and len(reviews) > 1:
            flags.append("identical_ratings")
            suspicion += 0.4
        
        # All 5 stars
        if all(r == 5.0 for r in ratings):
            flags.append("all_five_stars")
            suspicion += 0.3
        
        return ReviewerPattern(
            reviewer_name=reviewer_name,
            review_count=len(reviews),
            average_rating=round(avg_rating, 2),
            rating_variance=round(variance, 2),
            suspicion_score=min(1.0, round(suspicion, 2)),
            flags=flags
        )
    
    def _analyze_verification(self, reviews: List[Review]) -> Optional[ReviewerPattern]:
        """Analyze verification status patterns"""
        verified_count = sum(1 for r in reviews if r.verified_purchase)
        unverified_count = len(reviews) - verified_count
        
        if len(reviews) == 0:
            return None
        
        unverified_ratio = unverified_count / len(reviews)
        
        # If >threshold unverified, suspicious
        if unverified_ratio > settings.UNVERIFIED_THRESHOLD:
            return ReviewerPattern(
                reviewer_name="AGGREGATE_UNVERIFIED",
                review_count=unverified_count,
                average_rating=0.0,
                rating_variance=0.0,
                suspicion_score=round(min(1.0, unverified_ratio), 2),
                flags=[f"high_unverified_ratio_{unverified_ratio*100:.0f}%"]
            )
        
        return None