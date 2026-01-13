"""
Rate limiting middleware
"""
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status, Depends
from collections import defaultdict

from config import settings
from auth import verify_token

# Rate limiting storage (in-memory for now, use Redis in production)
rate_limit_storage = defaultdict(list)


async def check_rate_limit(request: Request, user_data: dict = Depends(verify_token)):
    """Rate limiting middleware"""
    user_id = user_data.get("sub")
    current_time = datetime.utcnow()
    
    # Clean old requests outside the window
    rate_limit_storage[user_id] = [
        req_time for req_time in rate_limit_storage[user_id]
        if current_time - req_time < timedelta(seconds=settings.RATE_LIMIT_WINDOW)
    ]
    
    # Check if limit exceeded
    if len(rate_limit_storage[user_id]) >= settings.RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds"
        )
    
    # Add current request
    rate_limit_storage[user_id].append(current_time)
    return user_id