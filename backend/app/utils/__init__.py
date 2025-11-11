"""
Utility modules for the AI Coach backend.
"""
from .logging import setup_logging
from .prompts import format_context_for_prompt, build_conversation_history

__all__ = [
    "setup_logging",
    "format_context_for_prompt",
    "build_conversation_history",
]
