"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    """Available agent types."""
    PROFESSIONAL_LEARNING = "professional_learning"
    CLASSROOM_CURRICULUM = "classroom_curriculum"


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    query: str = Field(..., min_length=1, max_length=2000, description="User's question")
    agent_id: AgentType = Field(..., description="Selected agent type")
    session_id: Optional[str] = Field(None, description="Optional session ID for context")


class Citation(BaseModel):
    """Citation information for retrieved documents."""
    id: str = Field(..., description="Unique citation identifier")
    source_title: str = Field(..., description="Title of source document")
    page_number: Optional[int] = Field(None, description="Page number if available")
    chunk_text: str = Field(..., description="Relevant text excerpt")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str = Field(..., description="AI-generated response")
    citations: List[Citation] = Field(default_factory=list, description="Source citations")
    agent_used: AgentType = Field(..., description="Agent that generated response")
    session_id: str = Field(..., description="Session identifier")
    message_id: str = Field(..., description="Unique message identifier")


class Message(BaseModel):
    """Individual message in a conversation."""
    role: str = Field(..., description="Message role: user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    citations: Optional[List[Citation]] = None
    message_id: Optional[str] = None


class SessionCreate(BaseModel):
    """Request schema for creating a new session."""
    agent_id: AgentType = Field(..., description="Initial agent for this session")
    title: Optional[str] = Field(None, max_length=200, description="Optional session title")


class SessionResponse(BaseModel):
    """Response schema for session data."""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User who owns this session")
    agent_id: AgentType = Field(..., description="Current agent for session")
    title: Optional[str] = Field(None, description="Session title")
    messages: List[Message] = Field(default_factory=list, description="Conversation history")
    created_at: datetime = Field(..., description="Session creation timestamp")
    last_accessed: datetime = Field(..., description="Last access timestamp")


class FeedbackRequest(BaseModel):
    """Request schema for submitting feedback."""
    message_id: str = Field(..., description="ID of message being rated")
    session_id: str = Field(..., description="Session ID")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    comment: Optional[str] = Field(None, max_length=1000, description="Optional feedback comment")


class FeedbackResponse(BaseModel):
    """Response schema for feedback submission."""
    feedback_id: str = Field(..., description="Unique feedback identifier")
    message: str = Field(default="Feedback received", description="Confirmation message")


class AgentInfo(BaseModel):
    """Information about an available agent."""
    agent_id: AgentType = Field(..., description="Agent identifier")
    name: str = Field(..., description="Agent display name")
    description: str = Field(..., description="Agent description")


class UserInfo(BaseModel):
    """User information from Firebase auth."""
    user_id: str = Field(..., description="Firebase user ID")
    email: Optional[str] = Field(None, description="User email")
    name: Optional[str] = Field(None, description="User display name")
    verified: bool = Field(default=True, description="Token verification status")
