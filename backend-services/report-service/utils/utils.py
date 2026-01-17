"""
Utility functions for Report Service
"""
import hashlib
from urllib.parse import urlparse
from datetime import datetime


def normalize_url(url: str) -> str:
    """
    Normalize URL for consistent hashing
    
    Args:
        url: URL to normalize
        
    Returns:
        Normalized URL string
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Remove 'www.' prefix
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Remove trailing slash from path
        path = parsed.path.rstrip('/')
        
        # Reconstruct normalized URL
        normalized = f"{parsed.scheme.lower()}://{domain}{path}"
        return normalized
    except Exception:
        return url


def generate_url_hash(url: str) -> str:
    """
    Generate SHA-256 hash for URL
    
    Args:
        url: URL to hash
        
    Returns:
        Hexadecimal hash string
    """
    normalized = normalize_url(url)
    return hashlib.sha256(normalized.encode()).hexdigest()


def generate_report_id(url_hash: str, timestamp: datetime) -> str:
    """
    Generate unique report ID
    
    Args:
        url_hash: Hash of the URL
        timestamp: Creation timestamp
        
    Returns:
        Unique 16-character report ID
    """
    combined = f"{url_hash}_{timestamp.isoformat()}"
    return hashlib.md5(combined.encode()).hexdigest()[:16]