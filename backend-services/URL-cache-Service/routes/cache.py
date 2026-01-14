"""
Cache management routes - Check, store, and invalidate cache
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import logging

from models import (
    CacheCheckResponse, 
    StoreCacheRequest, 
    CacheStoreResponse,
    InvalidateCacheRequest
)
from db.database import (
    get_cached_report,
    store_cached_report,
    invalidate_cached_report,
    cleanup_expired_cache
)
from utils.url_utils import generate_url_hash, normalize_url

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/check-cache", response_model=CacheCheckResponse)
async def check_cache(url: str):
    """
    Check if a valid cached report exists for the given URL
    
    Returns:
    - cached: Whether report exists
    - valid: Whether cache is still within TTL
    - report: The cached report data (if valid)
    - cached_at: When report was cached
    - expires_at: When cache will expire
    - age_days: How old the cache is
    """
    try:
        # Generate hash from normalized URL
        url_hash = generate_url_hash(url)
        
        # Retrieve from database
        cached_data = await get_cached_report(url_hash)
        
        if not cached_data:
            logger.info(f"Cache MISS for {url}")
            return CacheCheckResponse(
                cached=False,
                valid=False
            )
        
        # Check if cache is still valid
        now = datetime.utcnow()
        cached_at = cached_data.get("cached_at")
        expires_at = cached_data.get("expires_at")
        
        if expires_at and expires_at > now:
            # Cache is valid
            age = (now - cached_at).total_seconds() / 86400  # Convert to days
            
            logger.info(f"Cache HIT for {url} (age: {age:.2f} days)")
            
            return CacheCheckResponse(
                cached=True,
                valid=True,
                report=cached_data.get("report"),
                cached_at=cached_at.isoformat() if cached_at else None,
                expires_at=expires_at.isoformat() if expires_at else None,
                age_days=round(age, 2)
            )
        else:
            # Cache exists but expired
            logger.info(f"Cache EXPIRED for {url}")
            return CacheCheckResponse(
                cached=True,
                valid=False,
                cached_at=cached_at.isoformat() if cached_at else None,
                expires_at=expires_at.isoformat() if expires_at else None
            )
    
    except Exception as e:
        logger.error(f"Cache check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cache check failed: {str(e)}"
        )


@router.post("/store", response_model=CacheStoreResponse)
async def store_cache(request: StoreCacheRequest):
    """
    Store a new report in cache
    
    Args:
    - url: Product URL
    - report: Analysis report data
    - ttl_days: Cache validity in days (default: 7)
    """
    try:
        url_hash = generate_url_hash(request.url)
        normalized = normalize_url(request.url)
        
        success = await store_cached_report(
            url=request.url,
            url_hash=url_hash,
            normalized_url=normalized,
            report=request.report,
            ttl_days=request.ttl_days
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store cache"
            )
        
        expires_at = datetime.utcnow() + timedelta(days=request.ttl_days)
        
        return CacheStoreResponse(
            success=True,
            url_hash=url_hash,
            expires_at=expires_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cache storage failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cache storage failed: {str(e)}"
        )


@router.post("/invalidate")
async def invalidate_cache(request: InvalidateCacheRequest):
    """
    Force invalidate (delete) a cached report
    Useful when user requests force refresh
    """
    try:
        url_hash = generate_url_hash(request.url)
        success = await invalidate_cached_report(url_hash)
        
        return {
            "success": success,
            "message": "Cache invalidated" if success else "No cache found"
        }
    
    except Exception as e:
        logger.error(f"Cache invalidation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cache invalidation failed: {str(e)}"
        )


@router.post("/cleanup")
async def cleanup_cache():
    """
    Manually trigger cleanup of expired cache entries
    Normally handled automatically by MongoDB TTL index
    """
    try:
        deleted_count = await cleanup_expired_cache()
        return {
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Cleaned up {deleted_count} expired entries"
        }
    except Exception as e:
        logger.error(f"Cache cleanup failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cache cleanup failed: {str(e)}"
        )