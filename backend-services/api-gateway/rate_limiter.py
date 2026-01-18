"""
Rate limiting middleware
"""
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
from collections import defaultdict

from config import settings
# from utils.auth import verify_token  # Commented out for now

# Rate limiting storage (in-memory for now, use Redis in production)
rate_limit_storage = defaultdict(list)


async def check_rate_limit(request: Request):
    """
    Rate limiting middleware - IP-based (no authentication required)
    
    When authentication is re-enabled, you can switch back to user-based rate limiting
    by uncommenting the check_rate_limit_with_auth function below
    """
    # Use client IP as identifier instead of user_id
    client_ip = request.client.host
    
    # For development: also check X-Forwarded-For header (proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    identifier = forwarded_for.split(",")[0].strip() if forwarded_for else client_ip
    
    current_time = datetime.utcnow()
    
    # Clean old requests outside the window
    rate_limit_storage[identifier] = [
        req_time for req_time in rate_limit_storage[identifier]
        if current_time - req_time < timedelta(seconds=settings.RATE_LIMIT_WINDOW)
    ]
    
    # Check if limit exceeded
    if len(rate_limit_storage[identifier]) >= settings.RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds"
        )
    
    # Add current request
    rate_limit_storage[identifier].append(current_time)
    
    return None  # Return None since we don't need user_id anymore


# ============================================================================
# USER-BASED RATE LIMITING (for when auth is re-enabled)
# ============================================================================
# from utils.auth import verify_token
# 
# async def check_rate_limit_with_auth(request: Request, user_data: dict = Depends(verify_token)):
#     """Rate limiting middleware with user authentication"""
#     user_id = user_data.get("sub")
#     current_time = datetime.utcnow()
#     
#     # Clean old requests outside the window
#     rate_limit_storage[user_id] = [
#         req_time for req_time in rate_limit_storage[user_id]
#         if current_time - req_time < timedelta(seconds=settings.RATE_LIMIT_WINDOW)
#     ]
#     
#     # Check if limit exceeded
#     if len(rate_limit_storage[user_id]) >= settings.RATE_LIMIT_REQUESTS:
#         raise HTTPException(
#             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#             detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds"
#         )
#     
#     # Add current request
#     rate_limit_storage[user_id].append(current_time)
#     return user_id