"""
Utility functions for behavior analysis
"""
import re
from datetime import datetime
from typing import Optional
import logging

from config import settings

logger = logging.getLogger(__name__)


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse various date formats
    
    Args:
        date_str: Date string in various formats
    
    Returns:
        Parsed datetime object or None if parsing fails
    """
    if not date_str:
        return None
    
    # Clean the date string
    date_str = date_str.strip()
    
    # Try to extract date from strings like "Reviewed on January 15, 2026"
    date_str = re.sub(
        r'(Reviewed on|Posted on|Date:)\s*', 
        '', 
        date_str, 
        flags=re.IGNORECASE
    )
    
    # Try each format
    for fmt in settings.DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    # Try simple YYYY-MM-DD extraction
    match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_str)
    if match:
        try:
            return datetime(
                int(match.group(1)), 
                int(match.group(2)), 
                int(match.group(3))
            )
        except:
            pass
    
    logger.warning(f"Could not parse date: {date_str}")
    return None