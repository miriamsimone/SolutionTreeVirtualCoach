"""
Authentication routes for Firebase token verification.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.schemas import UserInfo
from app.services.firebase_service import FirebaseService
from app.dependencies import get_firebase_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/verify", response_model=UserInfo)
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    firebase_service: FirebaseService = Depends(get_firebase_service)
):
    """
    Verify Firebase ID token and return user information.

    Args:
        credentials: Bearer token from Authorization header
        firebase_service: Firebase service dependency

    Returns:
        UserInfo object with user details

    Raises:
        HTTPException: 401 if token is invalid
    """
    try:
        token = credentials.credentials
        user_info = await firebase_service.verify_token(token)
        logger.info(f"User verified: {user_info.user_id}")
        return user_info

    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
