"""
MongoDB connection management and database operations
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from config import settings

logger = logging.getLogger(__name__)

# MongoDB client (initialized on startup)
mongo_client: Optional[AsyncIOMotorClient] = None
db = None


async def startup_db_client():
    """Initialize MongoDB connection and create indexes"""
    global mongo_client, db
    
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
        db = mongo_client[settings.MONGO_DB]
        
        # Create indexes
        collection = db[settings.CACHE_COLLECTION]
        
        # Index on url_hash for fast lookups
        await collection.create_index("url_hash", unique=True)
        
        # TTL index - MongoDB will auto-delete expired documents
        await collection.create_index(
            "expires_at",
            expireAfterSeconds=0
        )
        
        # Index for cleanup queries
        await collection.create_index("cached_at")
        
        logger.info("MongoDB connected and indexes created")
        
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        raise


async def shutdown_db_client():
    """Close MongoDB connection"""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB connection closed")


def get_collection():
    """Get the cache collection"""
    return db[settings.CACHE_COLLECTION]


async def get_cached_report(url_hash: str) -> Optional[Dict[str, Any]]:
    """Retrieve cached report from MongoDB"""
    try:
        collection = get_collection()
        cached = await collection.find_one({"url_hash": url_hash})
        return cached
    except Exception as e:
        logger.error(f"Cache retrieval error: {str(e)}")
        return None


async def store_cached_report(
    url: str,
    url_hash: str,
    normalized_url: str,
    report: Dict[str, Any],
    ttl_days: int
) -> bool:
    """Store report in MongoDB with TTL"""
    try:
        collection = get_collection()
        
        now = datetime.utcnow()
        expires_at = now + timedelta(days=ttl_days)
        
        document = {
            "url_hash": url_hash,
            "original_url": url,
            "normalized_url": normalized_url,
            "report": report,
            "cached_at": now,
            "expires_at": expires_at,
            "ttl_days": ttl_days,
            "created_at": now,
            "updated_at": now
        }
        
        # Upsert: update if exists, insert if not
        result = await collection.update_one(
            {"url_hash": url_hash},
            {"$set": document},
            upsert=True
        )
        
        logger.info(f"Report cached for hash {url_hash}, expires: {expires_at}")
        return True
        
    except Exception as e:
        logger.error(f"Cache storage error: {str(e)}")
        return False


async def invalidate_cached_report(url_hash: str) -> bool:
    """Delete cached report"""
    try:
        collection = get_collection()
        result = await collection.delete_one({"url_hash": url_hash})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Cache invalidation error: {str(e)}")
        return False


async def cleanup_expired_cache():
    """Remove expired cache entries (called by cron job)"""
    try:
        collection = get_collection()
        result = await collection.delete_many({
            "expires_at": {"$lt": datetime.utcnow()}
        })
        logger.info(f"Cleaned up {result.deleted_count} expired cache entries")
        return result.deleted_count
    except Exception as e:
        logger.error(f"Cache cleanup error: {str(e)}")
        return 0


async def get_cache_statistics():
    """Get cache statistics"""
    try:
        collection = get_collection()
        
        total = await collection.count_documents({})
        valid = await collection.count_documents({
            "expires_at": {"$gt": datetime.utcnow()}
        })
        expired = total - valid
        
        # Get oldest and newest cache entries
        oldest = await collection.find_one(sort=[("cached_at", 1)])
        newest = await collection.find_one(sort=[("cached_at", -1)])
        
        return {
            "total_entries": total,
            "valid_entries": valid,
            "expired_entries": expired,
            "oldest_cache": oldest.get("cached_at").isoformat() if oldest else None,
            "newest_cache": newest.get("cached_at").isoformat() if newest else None,
        }
    except Exception as e:
        logger.error(f"Stats retrieval error: {str(e)}")
        return None