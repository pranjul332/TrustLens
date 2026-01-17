"""
Database operations for Report Service
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import logging

from config import settings
from utils.utils import generate_report_id, normalize_url

logger = logging.getLogger(__name__)

# MongoDB client (initialized on startup)
mongo_client: Optional[AsyncIOMotorClient] = None
db = None


async def connect_to_mongo():
    """Initialize MongoDB connection and create indexes"""
    global mongo_client, db
    
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
        db = mongo_client[settings.MONGO_DB]
        
        collection = db[settings.REPORTS_COLLECTION]
        
        # Create indexes
        await collection.create_index("url_hash", unique=True)
        await collection.create_index("metadata.expires_at", expireAfterSeconds=0)
        await collection.create_index("metadata.created_at")
        await collection.create_index("metadata.updated_at")
        
        logger.info("MongoDB connected and indexes created")
        
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB connection closed")


async def store_report_in_db(
    url: str,
    url_hash: str,
    report: Dict[str, Any],
    ttl_days: int
) -> str:
    """
    Store report in MongoDB
    
    Args:
        url: Original URL
        url_hash: Hash of the URL
        report: Report data
        ttl_days: Time-to-live in days
        
    Returns:
        Report ID
    """
    try:
        collection = db[settings.REPORTS_COLLECTION]
        
        now = datetime.utcnow()
        expires_at = now + timedelta(days=ttl_days)
        report_id = generate_report_id(url_hash, now)
        
        document = {
            "_id": report_id,
            "url": url,
            "url_hash": url_hash,
            "normalized_url": normalize_url(url),
            "report": report,
            "metadata": {
                "created_at": now,
                "updated_at": now,
                "expires_at": expires_at,
                "ttl_days": ttl_days,
                "access_count": 0,
                "last_accessed": None
            }
        }
        
        # Upsert based on url_hash (update if exists, insert if not)
        await collection.replace_one(
            {"url_hash": url_hash},
            document,
            upsert=True
        )
        
        logger.info(f"Report stored: {report_id} (expires: {expires_at})")
        return report_id
        
    except Exception as e:
        logger.error(f"Failed to store report: {str(e)}")
        raise


async def get_report_from_db(url_hash: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve report from MongoDB by URL hash
    
    Args:
        url_hash: Hash of the URL
        
    Returns:
        Report document or None if not found/expired
    """
    try:
        collection = db[settings.REPORTS_COLLECTION]
        
        # Find by url_hash
        document = await collection.find_one({"url_hash": url_hash})
        
        if not document:
            return None
        
        # Check if expired
        expires_at = document["metadata"]["expires_at"]
        if expires_at < datetime.utcnow():
            logger.info(f"Report expired: {document['_id']}")
            await collection.delete_one({"_id": document["_id"]})
            return None
        
        # Update access count
        await collection.update_one(
            {"_id": document["_id"]},
            {
                "$inc": {"metadata.access_count": 1},
                "$set": {"metadata.last_accessed": datetime.utcnow()}
            }
        )
        
        return document
        
    except Exception as e:
        logger.error(f"Failed to retrieve report: {str(e)}")
        return None


async def get_report_by_id(report_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve report by ID
    
    Args:
        report_id: Unique report identifier
        
    Returns:
        Report document or None if not found/expired
    """
    try:
        collection = db[settings.REPORTS_COLLECTION]
        document = await collection.find_one({"_id": report_id})
        
        if not document:
            return None
        
        # Check if expired
        expires_at = document["metadata"]["expires_at"]
        if expires_at < datetime.utcnow():
            await collection.delete_one({"_id": report_id})
            return None
        
        return document
        
    except Exception as e:
        logger.error(f"Failed to retrieve report by ID: {str(e)}")
        return None


async def delete_report_from_db(url_hash: str) -> bool:
    """
    Delete report from MongoDB
    
    Args:
        url_hash: Hash of the URL
        
    Returns:
        True if deleted, False otherwise
    """
    try:
        collection = db[settings.REPORTS_COLLECTION]
        result = await collection.delete_one({"url_hash": url_hash})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Failed to delete report: {str(e)}")
        return False


async def cleanup_expired_reports() -> int:
    """
    Remove expired reports
    
    Returns:
        Number of reports deleted
    """
    try:
        collection = db[settings.REPORTS_COLLECTION]
        result = await collection.delete_many({
            "metadata.expires_at": {"$lt": datetime.utcnow()}
        })
        logger.info(f"Cleaned up {result.deleted_count} expired reports")
        return result.deleted_count
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        return 0


async def get_all_reports(
    skip: int = 0,
    limit: int = 50,
    sort_by: str = "created_at"
) -> List[Dict[str, Any]]:
    """
    Get paginated list of reports
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        sort_by: Field to sort by
        
    Returns:
        List of report documents
    """
    try:
        collection = db[settings.REPORTS_COLLECTION]
        
        # Get reports, sorted and paginated
        cursor = collection.find(
            {"metadata.expires_at": {"$gt": datetime.utcnow()}}
        ).sort(f"metadata.{sort_by}", -1).skip(skip).limit(limit)
        
        reports = await cursor.to_list(length=limit)
        return reports
        
    except Exception as e:
        logger.error(f"Failed to list reports: {str(e)}")
        return []


async def get_stats() -> Dict[str, Any]:
    """
    Get report statistics
    
    Returns:
        Dictionary with statistics
    """
    try:
        collection = db[settings.REPORTS_COLLECTION]
        
        # Total reports
        total = await collection.count_documents({})
        
        # Active (not expired)
        active = await collection.count_documents({
            "metadata.expires_at": {"$gt": datetime.utcnow()}
        })
        
        # Expired
        expired = total - active
        
        # Most accessed
        most_accessed = await collection.find_one(
            sort=[("metadata.access_count", -1)]
        )
        
        # Average trust score
        pipeline = [
            {"$match": {"metadata.expires_at": {"$gt": datetime.utcnow()}}},
            {"$group": {
                "_id": None,
                "avg_trust_score": {"$avg": "$report.trust_score"},
                "avg_fake_percentage": {"$avg": "$report.fake_reviews_percentage"}
            }}
        ]
        
        agg_result = await collection.aggregate(pipeline).to_list(length=1)
        avg_scores = agg_result[0] if agg_result else {}
        
        return {
            "total_reports": total,
            "active_reports": active,
            "expired_reports": expired,
            "average_trust_score": round(avg_scores.get("avg_trust_score", 0), 2) if avg_scores else 0,
            "average_fake_percentage": round(avg_scores.get("avg_fake_percentage", 0), 2) if avg_scores else 0,
            "most_accessed_url": most_accessed.get("url") if most_accessed else None,
            "most_accessed_count": most_accessed["metadata"]["access_count"] if most_accessed else 0
        }
        
    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise


async def ping_database() -> bool:
    """
    Check database connection
    
    Returns:
        True if connected, False otherwise
    """
    try:
        await db.command("ping")
        return True
    except Exception:
        return False