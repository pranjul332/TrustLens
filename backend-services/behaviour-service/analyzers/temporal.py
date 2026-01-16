"""
Temporal pattern detection
"""
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from models import Review, TemporalPattern
from config import settings
from utils.utils import parse_date

logger = logging.getLogger(__name__)


class TemporalAnalyzer:
    """Detect temporal patterns and review bursts"""
    
    def analyze(self, reviews: List[Review]) -> List[TemporalPattern]:
        """
        Detect temporal anomalies:
        - Review bursts (many reviews in short time)
        - Rating spikes
        - Suspicious timing patterns
        
        Args:
            reviews: List of reviews to analyze
        
        Returns:
            List of detected temporal patterns
        """
        patterns = []
        
        # Parse dates
        dated_reviews = []
        for review in reviews:
            if review.date:
                parsed_date = parse_date(review.date)
                if parsed_date:
                    dated_reviews.append((parsed_date, review))
        
        if not dated_reviews:
            logger.warning("No valid dates found in reviews")
            return patterns
        
        # Sort by date
        dated_reviews.sort(key=lambda x: x[0])
        
        # Detect bursts (many reviews in short time)
        burst_patterns = self._detect_bursts(dated_reviews)
        patterns.extend(burst_patterns)
        
        # Detect rating spikes
        spike_patterns = self._detect_rating_spikes(dated_reviews)
        patterns.extend(spike_patterns)
        
        # Detect recency bias (too many recent reviews)
        recency_pattern = self._detect_recency_bias(dated_reviews)
        if recency_pattern:
            patterns.append(recency_pattern)
        
        return patterns
    
    def _detect_bursts(self, dated_reviews: List[tuple]) -> List[TemporalPattern]:
        """Detect review bursts (many reviews in short time window)"""
        patterns = []
        
        # Define time windows from config
        windows = [(days, f"{days} day{'s' if days > 1 else ''}") 
                   for days in settings.BURST_WINDOW_DAYS]
        
        for days, window_name in windows:
            # Count reviews in sliding window
            for i, (date, _) in enumerate(dated_reviews):
                window_end = date + timedelta(days=days)
                
                # Count reviews in this window
                reviews_in_window = []
                for j in range(i, len(dated_reviews)):
                    review_date, review = dated_reviews[j]
                    if review_date <= window_end:
                        reviews_in_window.append(review)
                    else:
                        break
                
                # Check if burst
                min_reviews = max(
                    settings.BURST_MIN_REVIEWS, 
                    len(dated_reviews) * settings.BURST_MIN_PERCENTAGE
                )
                
                if len(reviews_in_window) >= min_reviews:
                    avg_rating = sum(r.rating for r in reviews_in_window) / len(reviews_in_window)
                    
                    # Calculate suspicion score
                    # More reviews in shorter time = higher suspicion
                    concentration_ratio = len(reviews_in_window) / len(dated_reviews)
                    suspicion = min(1.0, concentration_ratio * (30 / days))
                    
                    patterns.append(TemporalPattern(
                        pattern_type="burst",
                        time_window=window_name,
                        review_count=len(reviews_in_window),
                        average_rating=round(avg_rating, 2),
                        suspicion_score=round(suspicion, 2),
                        description=f"{len(reviews_in_window)} reviews posted within {window_name} (suspicious burst)"
                    ))
                    break  # Only report most significant burst per window
        
        return patterns
    
    def _detect_rating_spikes(self, dated_reviews: List[tuple]) -> List[TemporalPattern]:
        """Detect sudden rating changes"""
        patterns = []
        
        if len(dated_reviews) < settings.MIN_REVIEWS_FOR_SPIKE:
            return patterns
        
        # Split into time periods
        total_days = (dated_reviews[-1][0] - dated_reviews[0][0]).days
        if total_days < settings.MIN_DAYS_FOR_TEMPORAL:
            return patterns
        
        # Divide into weeks
        weeks = defaultdict(list)
        for date, review in dated_reviews:
            week_num = (date - dated_reviews[0][0]).days // 7
            weeks[week_num].append(review)
        
        # Compare consecutive weeks
        week_nums = sorted(weeks.keys())
        for i in range(len(week_nums) - 1):
            week1 = weeks[week_nums[i]]
            week2 = weeks[week_nums[i + 1]]
            
            if (len(week1) >= settings.MIN_REVIEWS_PER_WEEK and 
                len(week2) >= settings.MIN_REVIEWS_PER_WEEK):
                avg1 = sum(r.rating for r in week1) / len(week1)
                avg2 = sum(r.rating for r in week2) / len(week2)
                
                # Detect spike (sudden increase)
                if avg2 - avg1 >= settings.SPIKE_RATING_THRESHOLD:
                    suspicion = min(1.0, (avg2 - avg1) / 2)
                    patterns.append(TemporalPattern(
                        pattern_type="rating_spike",
                        time_window=f"week {week_nums[i]} to {week_nums[i+1]}",
                        review_count=len(week2),
                        average_rating=round(avg2, 2),
                        suspicion_score=round(suspicion, 2),
                        description=f"Sudden rating increase from {avg1:.1f} to {avg2:.1f} stars"
                    ))
        
        return patterns
    
    def _detect_recency_bias(self, dated_reviews: List[tuple]) -> Optional[TemporalPattern]:
        """Detect if too many reviews are recent (possible fake campaign)"""
        if len(dated_reviews) < settings.MIN_REVIEWS_FOR_SPIKE:
            return None
        
        # Count reviews in last N days
        now = datetime.now()
        recent_cutoff = now - timedelta(days=settings.RECENCY_DAYS)
        
        recent_reviews = [r for date, r in dated_reviews if date >= recent_cutoff]
        recent_ratio = len(recent_reviews) / len(dated_reviews)
        
        # If >threshold of reviews are recent, suspicious
        if recent_ratio > settings.RECENCY_THRESHOLD:
            avg_rating = sum(r.rating for r in recent_reviews) / len(recent_reviews)
            
            return TemporalPattern(
                pattern_type="recency_bias",
                time_window=f"last {settings.RECENCY_DAYS} days",
                review_count=len(recent_reviews),
                average_rating=round(avg_rating, 2),
                suspicion_score=round(min(1.0, recent_ratio), 2),
                description=f"{recent_ratio*100:.0f}% of reviews posted in last {settings.RECENCY_DAYS} days (possible campaign)"
            )
        
        return None