"""
API route handlers for the AI Coach backend.
"""
from .auth import router as auth_router
from .chat import router as chat_router
from .sessions import router as sessions_router
from .feedback import router as feedback_router

__all__ = [
    "auth_router",
    "chat_router",
    "sessions_router",
    "feedback_router",
]
