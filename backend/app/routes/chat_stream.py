"""
Streaming chat route for real-time AI responses.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest, UserInfo, Message
from app.services.openai_service import OpenAIService
from app.services.pinecone_service import PineconeService
from app.services.firebase_service import FirebaseService
from app.services.agent_router import AgentRouter
from app.dependencies import get_current_user, get_firebase_service
from app.config import get_settings, Settings
from app.utils.prompts import build_conversation_history
import logging
import json
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


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: UserInfo = Depends(get_current_user),
    agent_router: AgentRouter = Depends(get_agent_router),
    firebase_service: FirebaseService = Depends(get_firebase_service),
    settings: Settings = Depends(get_settings)
):
    """
    Stream chat response in real-time for faster perceived performance.

    Returns Server-Sent Events (SSE) stream with:
    - citations (first event)
    - content chunks (streaming)
    - done event (last)
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
            session_id = await firebase_service.create_session(
                user_id=current_user.user_id,
                agent_id=request.agent_id.value,
                title=f"Chat with {request.agent_id.value}"
            )
            session = await firebase_service.get_session(
                current_user.user_id,
                session_id
            )

        # Build conversation history
        conversation_history = build_conversation_history(
            session.messages,
            max_history=settings.max_conversation_history
        )

        logger.info(
            f"Streaming chat for user {current_user.user_id}, "
            f"agent {request.agent_id.value}, session {session_id}"
        )

        # Retrieve context (citations) first
        citations = await agent_router.retrieve_context(
            request.query,
            request.agent_id
        )

        message_id = str(uuid.uuid4())

        async def generate():
            """Generate SSE stream."""
            try:
                # Send citations first
                yield f"data: {json.dumps({'type': 'citations', 'citations': [c.model_dump() for c in citations], 'session_id': session_id, 'message_id': message_id})}\n\n"

                # Stream response chunks
                system_prompt = agent_router.get_system_prompt(request.agent_id)
                full_response = ""

                async for chunk in agent_router.openai_service.generate_response_with_streaming(
                    system_prompt=system_prompt,
                    user_query=request.query,
                    citations=citations,
                    conversation_history=conversation_history
                ):
                    full_response += chunk
                    yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"

                # Send done event
                yield f"data: {json.dumps({'type': 'done'})}\n\n"

                # Save messages to Firebase in background
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
                        content=full_response,
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
                    logger.error(f"Failed to save messages: {e}")

            except Exception as e:
                logger.error(f"Streaming error: {e}")
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat stream failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )
