"""
Report listing and browsing endpoints
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import logging

from ..models import ReportListItem
from ..config import settings
from ..database import get_all_reports

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Listing"])


@router.get("/list")
async def list_reports(
    skip: int = 0,
    limit: int = 50,
    sort_by: str = "created_at"
):
    """
    List all active reports (paginated)
    
    Returns a paginated list of all non-expired reports with summary information.
    
    Args:
        skip: Number of records to skip (for pagination, default: 0)
        limit: Maximum number of records to return (max 100, default: 50)
        sort_by: Field to sort by - options: created_at, updated_at, expires_at (default: created_at)
        
    Returns:
        List of report summaries with pagination info
        
    Example:
        GET /reports/list?skip=0&limit=10&sort_by=created_at
    """
    try:
        # Validate limit
        limit = min(limit, settings.MAX_PAGE_SIZE)
        
        # Validate sort_by
        if sort_by not in settings.VALID_SORT_FIELDS:
            sort_by = settings.DEFAULT_SORT_FIELD
        
        reports = await get_all_reports(skip, limit, sort_by)
        
        # Transform to list items
        items = []
        now = datetime.utcnow()
        
        for doc in reports:
            metadata = doc["metadata"]
            report_data = doc.get("report", {})
            
            age = (now - metadata["created_at"]).total_seconds() / 86400
            
            items.append(ReportListItem(
                report_id=doc["_id"],
                url=doc["url"],
                trust_score=report_data.get("trust_score"),
                risk_level=report_data.get("risk_level"),
                created_at=metadata["created_at"].isoformat(),
                expires_at=metadata["expires_at"].isoformat(),
                age_days=round(age, 2)
            ))
        
        return {
            "success": True,
            "total": len(items),
            "skip": skip,
            "limit": limit,
            "sort_by": sort_by,
            "reports": items
        }
        
    except Exception as e:
        logger.error(f"Failed to list reports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list reports: {str(e)}"
        )