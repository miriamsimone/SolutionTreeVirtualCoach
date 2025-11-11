"""
Utilities for formatting prompts and context for LLM requests.
"""
from typing import List, Dict, Any
from app.models.schemas import Message, Citation


def format_context_for_prompt(citations: List[Citation]) -> str:
    """
    Format retrieved document chunks into context for the LLM prompt.

    Args:
        citations: List of citation objects from Pinecone retrieval

    Returns:
        Formatted context string
    """
    if not citations:
        return "No relevant context found in the knowledge base."

    context_parts = []
    for i, citation in enumerate(citations, 1):
        # Compact format to reduce tokens
        page_info = f" (p.{citation.page_number})" if citation.page_number else ""
        context_parts.append(f"[{i}] {citation.source_title}{page_info}: {citation.chunk_text}")

    return "\n\n".join(context_parts)


def build_conversation_history(
    messages: List[Message],
    max_history: int = 5
) -> List[Dict[str, str]]:
    """
    Build conversation history for multi-turn context.

    Args:
        messages: List of previous messages in the session
        max_history: Maximum number of message pairs to include

    Returns:
        List of message dicts in OpenAI format
    """
    if not messages:
        return []

    # Take the last N messages (where N = max_history * 2 for user + assistant pairs)
    recent_messages = messages[-(max_history * 2):]

    # Convert to OpenAI format
    history = []
    for msg in recent_messages:
        history.append({
            "role": msg.role,
            "content": msg.content
        })

    return history


def create_rag_prompt(
    system_prompt: str,
    user_query: str,
    context: str,
    conversation_history: List[Dict[str, str]] = None
) -> List[Dict[str, str]]:
    """
    Create complete message list for RAG-based chat completion.

    Args:
        system_prompt: Agent-specific system prompt
        user_query: Current user question
        context: Formatted context from retrieved documents
        conversation_history: Previous messages for multi-turn support

    Returns:
        List of messages for OpenAI chat completion
    """
    messages = []

    # System message with instructions
    messages.append({
        "role": "system",
        "content": system_prompt
    })

    # Add conversation history if available
    if conversation_history:
        messages.extend(conversation_history)

    # Add current query with context
    user_message = f"""Context from knowledge base:
{context}

User Question: {user_query}

Please provide a helpful response based on the context above. Include specific citations to support your answer."""

    messages.append({
        "role": "user",
        "content": user_message
    })

    return messages
