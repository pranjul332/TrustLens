"""
URL normalization and hashing utilities
"""
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import hashlib
import logging

from config import settings

logger = logging.getLogger(__name__)


def normalize_url(url: str) -> str:
    """
    Normalize product URL to ensure cache hits for equivalent URLs
    
    Examples:
    - Remove tracking parameters (utm_source, ref, etc.)
    - Sort query parameters
    - Lowercase domain
    - Remove www. prefix
    - Extract product ID for consistent caching
    """
    try:
        parsed = urlparse(url)
        
        # Normalize domain (lowercase, remove www.)
        domain = parsed.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Parse and filter query parameters
        params = parse_qs(parsed.query)
        
        # Keep only essential parameters
        filtered_params = {
            k: v for k, v in params.items() 
            if k.lower() not in settings.TRACKING_PARAMS
        }
        
        # Sort parameters for consistency
        sorted_query = urlencode(sorted(filtered_params.items()), doseq=True)
        
        # Reconstruct URL
        normalized = urlunparse((
            parsed.scheme.lower(),
            domain,
            parsed.path.rstrip('/'),
            '',  # params
            sorted_query,
            ''   # fragment
        ))
        
        logger.info(f"Normalized URL: {url} -> {normalized}")
        return normalized
        
    except Exception as e:
        logger.error(f"URL normalization failed: {str(e)}")
        return url


def generate_url_hash(url: str) -> str:
    """Generate consistent hash for normalized URL"""
    normalized = normalize_url(url)
    return hashlib.sha256(normalized.encode()).hexdigest()