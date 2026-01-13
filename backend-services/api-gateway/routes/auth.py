"""
Authentication routes - Login and Registration
"""
from fastapi import APIRouter
import logging

from models import LoginRequest, RegisterRequest, TokenResponse
from utils.auth import create_access_token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    """Register new user (simplified - implement proper user storage)"""
    # TODO: Implement actual user registration with database
    # For now, just create a token
    logger.info(f"User registration attempt: {request.email}")
    
    token_data = {
        "sub": request.email,
        "name": request.name,
        "type": "access"
    }
    access_token = create_access_token(token_data)
    
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login endpoint (simplified - implement proper authentication)"""
    # TODO: Implement actual authentication with database
    # For now, accept any login and create token
    logger.info(f"Login attempt: {request.email}")
    
    token_data = {
        "sub": request.email,
        "type": "access"
    }
    access_token = create_access_token(token_data)
    
    return TokenResponse(access_token=access_token)