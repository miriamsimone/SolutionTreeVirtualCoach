"""
Session management routes for conversation history.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.schemas import SessionCreate, SessionResponse, UserInfo
from app.services.firebase_service import FirebaseService
from app.dependencies import get_current_user, get_firebase_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: SessionCreate,
    current_user: UserInfo = Depends(get_current_user),
    firebase_service: FirebaseService = Depends(get_firebase_service)
):
    """
    Create a new chat session.

    Args:
        request: Session creation request with agent_id and optional title
        current_user: Authenticated user information
        firebase_service: Firebase service

    Returns:
        Created SessionResponse object

    Raises:
        HTTPException: 500 if session creation fails
    """
    try:
        session_id = await firebase_service.create_session(
            user_id=current_user.user_id,
            agent_id=request.agent_id.value,
            title=request.title
        )

        session = await firebase_service.get_session(
            current_user.user_id,
            session_id
        )

        logger.info(f"Created session {session_id} for user {current_user.user_id}")
        return session

    except Exception as e:
        logger.error(f"Failed to create session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session"
        )


@router.get("", response_model=List[SessionResponse])
async def get_sessions(
    current_user: UserInfo = Depends(get_current_user),
    firebase_service: FirebaseService = Depends(get_firebase_service),
    limit: int = 50
):
    """
    Get all sessions for the authenticated user.

    Args:
        current_user: Authenticated user information
        firebase_service: Firebase service
        limit: Maximum number of sessions to return

    Returns:
        List of SessionResponse objects

    Raises:
        HTTPException: 500 if retrieval fails
    """
    try:
        sessions = await firebase_service.get_user_sessions(
            user_id=current_user.user_id,
            limit=limit
        )

        logger.info(f"Retrieved {len(sessions)} sessions for user {current_user.user_id}")
        return sessions

    except Exception as e:
        logger.error(f"Failed to get sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sessions"
        )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: UserInfo = Depends(get_current_user),
    firebase_service: FirebaseService = Depends(get_firebase_service)
):
    """
    Get a specific session by ID.

    Args:
        session_id: Session ID to retrieve
        current_user: Authenticated user information
        firebase_service: Firebase service

    Returns:
        SessionResponse object

    Raises:
        HTTPException: 404 if session not found, 500 for other errors
    """
    try:
        session = await firebase_service.get_session(
            current_user.user_id,
            session_id
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )

        logger.info(f"Retrieved session {session_id} for user {current_user.user_id}")
        return session

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session"
        )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    current_user: UserInfo = Depends(get_current_user),
    firebase_service: FirebaseService = Depends(get_firebase_service)
):
    """
    Delete a session.

    Args:
        session_id: Session ID to delete
        current_user: Authenticated user information
        firebase_service: Firebase service

    Raises:
        HTTPException: 404 if session not found, 500 for other errors
    """
    try:
        # Verify session exists and belongs to user
        session = await firebase_service.get_session(
            current_user.user_id,
            session_id
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )

        await firebase_service.delete_session(
            current_user.user_id,
            session_id
        )

        logger.info(f"Deleted session {session_id} for user {current_user.user_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete session"
        )
