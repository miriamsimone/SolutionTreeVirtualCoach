"""
FastAPI dependencies for authentication and service injection.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.config import Settings, get_settings
from app.services.firebase_service import FirebaseService
from app.models.schemas import UserInfo
import logging

logger = logging.getLogger(__name__)

# Security scheme for Bearer token
security = HTTPBearer()


async def get_firebase_service(
    settings: Settings = Depends(get_settings)
) -> FirebaseService:
    """Dependency to get Firebase service instance."""
    return FirebaseService(settings)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    firebase_service: FirebaseService = Depends(get_firebase_service)
) -> UserInfo:
    """
    Validate Firebase auth token and return user information.

    Raises:
        HTTPException: If token is invalid or verification fails
    """
    try:
        token = credentials.credentials
        user_info = await firebase_service.verify_token(token)
        return user_info
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    firebase_service: FirebaseService = Depends(get_firebase_service)
) -> Optional[UserInfo]:
    """
    Optional authentication - returns user if token provided and valid, None otherwise.
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        user_info = await firebase_service.verify_token(token)
        return user_info
    except Exception as e:
        logger.warning(f"Optional auth failed: {str(e)}")
        return None
