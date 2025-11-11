"""
Agent routing service for managing different AI coaching agents.
"""
from typing import Dict, Any, List
from app.config import Settings
from app.models.schemas import AgentType, Citation
from app.services.openai_service import OpenAIService
from app.services.pinecone_service import PineconeService
import logging

logger = logging.getLogger(__name__)


class AgentRouter:
    """Service for routing queries to appropriate agents with their configurations."""

    def __init__(
        self,
        settings: Settings,
        openai_service: OpenAIService,
        pinecone_service: PineconeService
    ):
        """
        Initialize agent router.

        Args:
            settings: Application settings
            openai_service: OpenAI service instance
            pinecone_service: Pinecone service instance
        """
        self.settings = settings
        self.openai_service = openai_service
        self.pinecone_service = pinecone_service
        self.agent_configs = settings.agent_configs

    def get_agent_config(self, agent_id: AgentType) -> Dict[str, Any]:
        """
        Get configuration for a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent configuration dict

        Raises:
            ValueError: If agent_id is not recognized
        """
        config = self.agent_configs.get(agent_id.value)
        if not config:
            raise ValueError(f"Unknown agent: {agent_id}")
        return config

    def get_system_prompt(self, agent_id: AgentType) -> str:
        """
        Get system prompt for a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            System prompt string
        """
        config = self.get_agent_config(agent_id)
        return config["system_prompt"]

    def get_metadata_filter(self, agent_id: AgentType) -> Dict[str, Any]:
        """
        Get Pinecone metadata filter for a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Metadata filter dict
        """
        config = self.get_agent_config(agent_id)
        return config["metadata_filter"]

    async def retrieve_context(
        self,
        query: str,
        agent_id: AgentType
    ) -> List[Citation]:
        """
        Retrieve relevant context for a query using agent-specific filtering.

        Args:
            query: User's question
            agent_id: Agent to use for retrieval

        Returns:
            List of Citation objects with retrieved documents
        """
        try:
            # Generate query embedding
            query_embedding = await self.openai_service.get_embedding(query)

            # Get agent-specific metadata filter
            metadata_filter = self.get_metadata_filter(agent_id)

            # Query Pinecone with agent filter
            citations = await self.pinecone_service.query_documents(
                query_embedding=query_embedding,
                metadata_filter=metadata_filter
            )

            logger.info(
                f"Retrieved {len(citations)} documents for agent '{agent_id.value}'"
            )
            return citations

        except Exception as e:
            logger.error(f"Context retrieval failed: {str(e)}")
            raise

    async def generate_response(
        self,
        query: str,
        agent_id: AgentType,
        conversation_history: List[Dict[str, str]] = None
    ) -> tuple[str, List[Citation]]:
        """
        Generate agent response with RAG context.

        Args:
            query: User's question
            agent_id: Agent to use
            conversation_history: Previous messages for context

        Returns:
            Tuple of (response_text, citations)
        """
        try:
            # Retrieve context
            citations = await self.retrieve_context(query, agent_id)

            # Get agent system prompt
            system_prompt = self.get_system_prompt(agent_id)

            # Generate response
            response_text = await self.openai_service.generate_chat_response(
                system_prompt=system_prompt,
                user_query=query,
                citations=citations,
                conversation_history=conversation_history
            )

            return response_text, citations

        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            raise

    def list_available_agents(self) -> List[Dict[str, str]]:
        """
        Get list of all available agents.

        Returns:
            List of dicts with agent info
        """
        agents = []
        for agent_id, config in self.agent_configs.items():
            agents.append({
                "agent_id": agent_id,
                "name": config["name"],
                "description": config["description"]
            })
        return agents
