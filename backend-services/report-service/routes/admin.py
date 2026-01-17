"""
Administrative operations and maintenance endpoints
"""
from fastapi import APIRouter, HTTPException, status
import logging

from db.database import cleanup_expired_reports, get_stats

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Administration"])


@router.post("/cleanup")
async def cleanup_reports():
    """
    Manually trigger cleanup of expired reports
    
    Normally, expired reports are handled automatically by MongoDB's TTL index.
    This endpoint allows manual cleanup if needed for maintenance purposes.
    
    Returns:
        Number of reports deleted
        
    Note:
        This is redundant with MongoDB's automatic TTL cleanup but useful for:
        - Testing
        - Forcing immediate cleanup
        - Verifying TTL functionality
    """
    try:
        deleted_count = await cleanup_expired_reports()
        return {
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Cleaned up {deleted_count} expired reports"
        }
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cleanup failed: {str(e)}"
        )


@router.get("/stats")
async def get_stats_route():
    """
    Get comprehensive report statistics
    
    Returns analytics about the report database including:
    - Total, active, and expired report counts
    - Average trust scores
    - Average fake review percentages
    - Most accessed reports
    
    Returns:
        Statistics dictionary with aggregated metrics
        
    Example Response:
        {
            "total_reports": 150,
            "active_reports": 120,
            "expired_reports": 30,
            "average_trust_score": 72.5,
            "average_fake_percentage": 18.3,
            "most_accessed_url": "https://example.com/product",
            "most_accessed_count": 45
        }
    """
    try:
        stats = await get_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )