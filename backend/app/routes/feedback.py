"""
Feedback routes for user ratings and comments.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import FeedbackRequest, FeedbackResponse, UserInfo
from app.services.firebase_service import FirebaseService
from app.dependencies import get_current_user, get_firebase_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    request: FeedbackRequest,
    current_user: UserInfo = Depends(get_current_user),
    firebase_service: FirebaseService = Depends(get_firebase_service)
):
    """
    Submit feedback/rating for a chat response.

    Args:
        request: Feedback request with message_id, session_id, rating, and optional comment
        current_user: Authenticated user information
        firebase_service: Firebase service

    Returns:
        FeedbackResponse with confirmation

    Raises:
        HTTPException: 400 for invalid input, 500 for server errors
    """
    try:
        # Verify session exists and belongs to user
        session = await firebase_service.get_session(
            current_user.user_id,
            request.session_id
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {request.session_id} not found"
            )

        # Save feedback
        feedback_id = await firebase_service.save_feedback(
            user_id=current_user.user_id,
            session_id=request.session_id,
            message_id=request.message_id,
            rating=request.rating,
            comment=request.comment
        )

        logger.info(
            f"Feedback {feedback_id} submitted for message {request.message_id} "
            f"by user {current_user.user_id}"
        )

        return FeedbackResponse(
            feedback_id=feedback_id,
            message="Feedback received successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to submit feedback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback"
        )
