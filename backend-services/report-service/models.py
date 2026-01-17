"""
Pydantic models for Report Service
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class StoreReportRequest(BaseModel):
    """Request model for storing a report"""
    url: str
    report: Dict[str, Any]
    ttl_days: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/product/123",
                "report": {
                    "trust_score": 75,
                    "risk_level": "medium",
                    "fake_reviews_percentage": 25.5
                },
                "ttl_days": 7
            }
        }


class StoreReportResponse(BaseModel):
    """Response model for storing a report"""
    success: bool
    report_id: str
    url_hash: str
    expires_at: str
    message: str


class GetReportResponse(BaseModel):
    """Response model for retrieving a report"""
    success: bool
    report: Dict[str, Any]
    metadata: Dict[str, Any]
    cached_at: str
    expires_at: str
    age_days: float


class ReportMetadata(BaseModel):
    """Internal metadata for reports"""
    url: str
    url_hash: str
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    access_count: int
    last_accessed: Optional[datetime] = None


class ReportListItem(BaseModel):
    """Summary model for report listings"""
    report_id: str
    url: str
    trust_score: Optional[int] = None
    risk_level: Optional[str] = None
    created_at: str
    expires_at: str
    age_days: float


class HealthResponse(BaseModel):
    """Health check response"""
    service: str
    mongodb: str
    timestamp: str


class StatsResponse(BaseModel):
    """Statistics response"""
    total_reports: int
    active_reports: int
    expired_reports: int
    average_trust_score: float
    average_fake_percentage: float
    most_accessed_url: Optional[str]
    most_accessed_count: int