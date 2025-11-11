"""
Chat routes for AI coaching conversations.
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.models.schemas import ChatRequest, ChatResponse, UserInfo, AgentInfo, AgentType, Message
from app.services.openai_service import OpenAIService
from app.services.pinecone_service import PineconeService
from app.services.firebase_service import FirebaseService
from app.services.agent_router import AgentRouter
from app.dependencies import get_current_user, get_firebase_service
from app.config import get_settings, Settings
from app.utils.prompts import build_conversation_history
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


def get_agent_router(
    settings: Settings = Depends(get_settings)
) -> AgentRouter:
    """Dependency to create AgentRouter instance."""
    openai_service = OpenAIService(settings)
    pinecone_service = PineconeService(settings)
    return AgentRouter(settings, openai_service, pinecone_service)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: UserInfo = Depends(get_current_user),
    agent_router: AgentRouter = Depends(get_agent_router),
    firebase_service: FirebaseService = Depends(get_firebase_service),
    settings: Settings = Depends(get_settings)
):
    """
    Process chat request and return AI-generated response with citations.

    Args:
        request: Chat request with query, agent_id, and optional session_id
        current_user: Authenticated user information
        agent_router: Agent routing service
        firebase_service: Firebase service for session management
        settings: Application settings

    Returns:
        ChatResponse with AI response, citations, and session info

    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    try:
        # Get or create session
        if request.session_id:
            session = await firebase_service.get_session(
                current_user.user_id,
                request.session_id
            )
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Session {request.session_id} not found"
                )
            session_id = request.session_id
        else:
            # Create new session
            session_id = await firebase_service.create_session(
                user_id=current_user.user_id,
                agent_id=request.agent_id.value,
                title=f"Chat with {request.agent_id.value}"
            )
            session = await firebase_service.get_session(
                current_user.user_id,
                session_id
            )

        # Build conversation history for multi-turn support
        conversation_history = build_conversation_history(
            session.messages,
            max_history=settings.max_conversation_history
        )

        logger.info(
            f"Processing chat request for user {current_user.user_id}, "
            f"agent {request.agent_id.value}, session {session_id}"
        )

        # Generate response using agent router
        response_text, citations = await agent_router.generate_response(
            query=request.query,
            agent_id=request.agent_id,
            conversation_history=conversation_history
        )

        # Create message ID
        message_id = str(uuid.uuid4())

        # Build response immediately
        chat_response = ChatResponse(
            response=response_text,
            citations=citations,
            agent_used=request.agent_id,
            session_id=session_id,
            message_id=message_id
        )

        # Save messages to Firebase in background (non-blocking)
        async def save_messages():
            try:
                user_message = Message(
                    role="user",
                    content=request.query,
                    timestamp=datetime.utcnow(),
                    message_id=str(uuid.uuid4())
                )
                await firebase_service.add_message_to_session(
                    current_user.user_id,
                    session_id,
                    user_message
                )

                assistant_message = Message(
                    role="assistant",
                    content=response_text,
                    timestamp=datetime.utcnow(),
                    message_id=message_id,
                    citations=citations
                )
                await firebase_service.add_message_to_session(
                    current_user.user_id,
                    session_id,
                    assistant_message
                )
                logger.info(f"Messages saved to session {session_id}")
            except Exception as e:
                logger.error(f"Failed to save messages to Firebase: {e}")

        background_tasks.add_task(save_messages)

        logger.info(f"Chat response generated successfully for session {session_id}")
        return chat_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat request failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.get("/agents", response_model=list[AgentInfo])
async def list_agents(
    agent_router: AgentRouter = Depends(get_agent_router)
):
    """
    Get list of available AI coaching agents.

    Args:
        agent_router: Agent routing service

    Returns:
        List of AgentInfo objects
    """
    try:
        agents_data = agent_router.list_available_agents()
        agents = [
            AgentInfo(
                agent_id=AgentType(agent["agent_id"]),
                name=agent["name"],
                description=agent["description"]
            )
            for agent in agents_data
        ]
        return agents

    except Exception as e:
        logger.error(f"Failed to list agents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agent list"
        )
