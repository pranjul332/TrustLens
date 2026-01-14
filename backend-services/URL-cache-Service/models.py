"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

from config import settings


class CheckCacheRequest(BaseModel):
    url: str


class CacheCheckResponse(BaseModel):
    cached: bool
    valid: bool
    report: Optional[Dict[str, Any]] = None
    cached_at: Optional[str] = None
    expires_at: Optional[str] = None
    age_days: Optional[float] = None


class StoreCacheRequest(BaseModel):
    url: str
    report: Dict[str, Any]
    ttl_days: Optional[int] = settings.CACHE_TTL_DAYS


class CacheStoreResponse(BaseModel):
    success: bool
    url_hash: str
    expires_at: str


class InvalidateCacheRequest(BaseModel):
    url: str