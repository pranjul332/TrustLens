from fastapi import APIRouter
from datetime import datetime
from db.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        db = get_db()
        await db.command("ping")
        mongo_status = "connected"
    except Exception as e:
        mongo_status = f"disconnected: {str(e)}"

    return {
        "service": "healthy",
        "mongodb": mongo_status,
        "timestamp": datetime.utcnow().isoformat()
    }
