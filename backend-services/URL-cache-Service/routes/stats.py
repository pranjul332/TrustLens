from fastapi import APIRouter, HTTPException, status
import logging

from config import settings
from db.database import get_cache_statistics

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/stats")
async def cache_stats():
    """Get cache statistics"""
    try:
        stats = await get_cache_statistics()
        
        if stats is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve statistics"
            )
        
        # Add TTL configuration to stats
        stats["cache_ttl_days"] = settings.CACHE_TTL_DAYS
        
        return stats
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Stats retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stats retrieval failed: {str(e)}"
        )