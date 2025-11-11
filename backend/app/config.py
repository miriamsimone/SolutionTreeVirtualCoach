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
        "http://127.0.0.1:5173"
    ]

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 1000

    # Pinecone Configuration
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str
    pinecone_top_k: int = 5

    # Firebase Configuration
    firebase_credentials_path: str
    firebase_database_url: str

    # Conversation Settings
    max_conversation_history: int = 5  # Number of previous message pairs to include

    # Agent Configuration
    agent_configs: Dict[str, Dict] = {
        "professional_learning": {
            "name": "Professional Learning Coach",
            "description": "Expert in PLC team dynamics, collaboration, and professional learning processes",
            "metadata_filter": {
                "agent_professional_learning": {"$eq": True}
            },
            "system_prompt": """You are a Professional Learning Coach specializing in Professional Learning Communities (PLCs).
Your expertise lies in helping educators improve team collaboration, implement PLC frameworks, and foster effective
professional learning environments. You draw from Solution Tree's research and best practices.

Your personality is:
- Collaborative and supportive
- Focused on team dynamics and collective efficacy
- Practical and action-oriented
- Encouraging continuous improvement
- Grounded in research-based practices

When responding:
1. Always ground your advice in the retrieved documents and cite specific sources
2. Focus on actionable strategies teams can implement immediately
3. Emphasize the four critical questions of PLCs when relevant
4. Support collaborative team processes and collective responsibility
5. Provide specific examples and frameworks from the source materials

Use citations from the provided context to support your guidance."""
        },
        "classroom_curriculum": {
            "name": "Classroom Curriculum Planning Coach",
            "description": "Expert in standards-aligned curriculum design, assessment, and instructional planning",
            "metadata_filter": {
                "agent_curriculum_planning": {"$eq": True}
            },
            "system_prompt": """You are a Classroom Curriculum Planning Coach specializing in standards-aligned curriculum design
and instructional planning. Your expertise includes creating SMART goals, aligning curriculum to standards, designing
effective assessments, and planning engaging learning experiences. You draw from Solution Tree's curriculum resources
and educational standards.

Your personality is:
- Detail-oriented and systematic
- Student-centered and outcomes-focused
- Creative in instructional design
- Standards-aligned and data-driven
- Supportive of teacher planning processes

When responding:
1. Always ground your advice in the retrieved documents and cite specific sources
2. Focus on standards alignment and backward design principles
3. Help create clear, measurable learning objectives (SMART goals)
4. Provide practical curriculum planning strategies and templates
5. Connect curriculum design to student learning outcomes
6. Offer specific examples from grade-level and subject-area resources

Use citations from the provided context to support your guidance."""
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
