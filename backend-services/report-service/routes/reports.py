"""
CRUD operations for reports
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import logging

from ..models import (
    StoreReportRequest,
    StoreReportResponse,
    GetReportResponse
)
from ..config import settings
from ..utils import generate_url_hash
from ..database import (
    store_report_in_db,
    get_report_from_db,
    get_report_by_id,
    delete_report_from_db
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/store", response_model=StoreReportResponse)
async def store_report(request: StoreReportRequest):
    """
    Store analysis report with TTL
    
    The report will be automatically deleted after ttl_days.
    If a report already exists for the URL, it will be replaced.
    
    Args:
        request: Report data including URL, report content, and optional TTL
        
    Returns:
        Confirmation with report ID and expiration time
    """
    try:
        ttl_days = request.ttl_days or settings.DEFAULT_TTL_DAYS
        url_hash = generate_url_hash(request.url)
        
        report_id = await store_report_in_db(
            url=request.url,
            url_hash=url_hash,
            report=request.report,
            ttl_days=ttl_days
        )
        
        expires_at = datetime.utcnow() + timedelta(days=ttl_days)
        
        return StoreReportResponse(
            success=True,
            report_id=report_id,
            url_hash=url_hash,
            expires_at=expires_at.isoformat(),
            message=f"Report stored successfully, expires in {ttl_days} days"
        )
        
    except Exception as e:
        logger.error(f"Failed to store report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store report: {str(e)}"
        )


@router.get("/get", response_model=GetReportResponse)
async def get_report(url: str):
    """
    Retrieve report by product URL
    
    Returns the most recent report for the given URL.
    Increments the access counter each time the report is retrieved.
    
    Args:
        url: Product URL to look up
        
    Returns:
        Report data with metadata (age, expiration, access count)
        
    Raises:
        404: Report not found or expired
    """
    try:
        url_hash = generate_url_hash(url)
        document = await get_report_from_db(url_hash)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found or expired"
            )
        
        metadata = document["metadata"]
        created_at = metadata["created_at"]
        expires_at = metadata["expires_at"]
        age = (datetime.utcnow() - created_at).total_seconds() / 86400
        
        return GetReportResponse(
            success=True,
            report=document["report"],
            metadata={
                "report_id": document["_id"],
                "url": document["url"],
                "access_count": metadata["access_count"],
                "ttl_days": metadata["ttl_days"]
            },
            cached_at=created_at.isoformat(),
            expires_at=expires_at.isoformat(),
            age_days=round(age, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve report: {str(e)}"
        )


@router.get("/get/{report_id}", response_model=GetReportResponse)
async def get_report_by_id_route(report_id: str):
    """
    Retrieve report by report ID
    
    Direct lookup using the unique report identifier.
    
    Args:
        report_id: Unique report identifier
        
    Returns:
        Report data with metadata
        
    Raises:
        404: Report not found or expired
    """
    try:
        document = await get_report_by_id(report_id)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found or expired"
            )
        
        metadata = document["metadata"]
        created_at = metadata["created_at"]
        expires_at = metadata["expires_at"]
        age = (datetime.utcnow() - created_at).total_seconds() / 86400
        
        return GetReportResponse(
            success=True,
            report=document["report"],
            metadata={
                "report_id": document["_id"],
                "url": document["url"],
                "access_count": metadata["access_count"],
                "ttl_days": metadata["ttl_days"]
            },
            cached_at=created_at.isoformat(),
            expires_at=expires_at.isoformat(),
            age_days=round(age, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve report: {str(e)}"
        )


@router.delete("/delete")
async def delete_report(url: str):
    """
    Delete report for a given URL
    
    Permanently removes the report from the database.
    
    Args:
        url: Product URL whose report should be deleted
        
    Returns:
        Success confirmation
        
    Raises:
        404: Report not found
    """
    try:
        url_hash = generate_url_hash(url)
        success = await delete_report_from_db(url_hash)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        return {
            "success": True,
            "message": "Report deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete report: {str(e)}"
        )