"""
Configuration management for the AI Coach backend.
"""
from pydantic_settings import BaseSettings
from typing import Dict, List
from functools import lru_cache
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    app_name: str = "AI PLC Coach API"
    app_version: str = "1.0.0"
    debug: bool = False

    # CORS Settings (allow frontend origins)
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://solutiontreevirtualcoach.web.app",
        "https://solutiontreevirtualcoach.firebaseapp.com"
    ]

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"  # Fast and cost-effective
    openai_temperature: float = 0.7
    openai_max_tokens: int = 500  # Reduced for faster responses (aim for concise answers)

    # Pinecone Configuration
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str
    pinecone_top_k: int = 3  # Reduced from 5 for faster responses

    # Firebase Configuration
    firebase_project_id: str
    firebase_private_key: str
    firebase_client_email: str
    firebase_database_url: str

    # Conversation Settings
    max_conversation_history: int = 2  # Number of previous message pairs to include (reduced for speed)

    # Agent Configuration
    agent_configs: Dict[str, Dict] = {
        "professional_learning": {
            "name": "Professional Learning Coach",
            "description": "Expert in PLC team dynamics, collaboration, and professional learning processes",
            "metadata_filter": {
                "agent_professional_learning": {"$eq": True}
            },
            "system_prompt": """You are a Professional Learning Coach for PLCs. You help educators with team collaboration and PLC implementation using Solution Tree research.

Be collaborative, practical, and action-oriented. Always cite sources from the provided context. Focus on actionable strategies and the four critical PLC questions. Keep responses concise and specific."""
        },
        "classroom_curriculum": {
            "name": "Classroom Curriculum Planning Coach",
            "description": "Expert in standards-aligned curriculum design, assessment, and instructional planning",
            "metadata_filter": {
                "agent_curriculum_planning": {"$eq": True}
            },
            "system_prompt": """You are a Curriculum Planning Coach specializing in standards-aligned design and SMART goals. You help educators plan curriculum using Solution Tree resources.

Be systematic, student-centered, and data-driven. Always cite sources from the provided context. Focus on standards alignment, backward design, and measurable objectives. Keep responses concise and practical."""
        }
    }

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",  # Ignore extra fields from .env
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
