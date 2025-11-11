"""
OpenAI service for LLM interactions and embeddings.
"""
from typing import List, Dict, Any, Tuple
from openai import AsyncOpenAI
import logging
from app.config import Settings
from app.models.schemas import Citation
from app.utils.prompts import create_rag_prompt, format_context_for_prompt

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self, settings: Settings):
        """
        Initialize OpenAI service.

        Args:
            settings: Application settings containing OpenAI configuration
        """
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using OpenAI.

        Args:
            text: Input text to embed

        Returns:
            Embedding vector as list of floats
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
                dimensions=1024  # Match Pinecone index dimension
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding for text of length {len(text)}")
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise

    async def generate_chat_response(
        self,
        system_prompt: str,
        user_query: str,
        citations: List[Citation],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate chat completion response using RAG context.

        Args:
            system_prompt: Agent-specific system prompt
            user_query: User's question
            citations: Retrieved documents for context
            conversation_history: Previous messages for multi-turn support

        Returns:
            AI-generated response text
        """
        try:
            # Format context from citations
            context = format_context_for_prompt(citations)

            # Build complete message list
            messages = create_rag_prompt(
                system_prompt=system_prompt,
                user_query=user_query,
                context=context,
                conversation_history=conversation_history or []
            )

            # Generate response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            response_text = response.choices[0].message.content
            logger.info(f"Generated response of length {len(response_text)}")

            return response_text

        except Exception as e:
            logger.error(f"Failed to generate chat response: {str(e)}")
            raise

    async def generate_response_with_streaming(
        self,
        system_prompt: str,
        user_query: str,
        citations: List[Citation],
        conversation_history: List[Dict[str, str]] = None
    ):
        """
        Generate streaming chat completion response.

        Args:
            system_prompt: Agent-specific system prompt
            user_query: User's question
            citations: Retrieved documents for context
            conversation_history: Previous messages for multi-turn support

        Yields:
            Response chunks as they arrive
        """
        try:
            # Format context from citations
            context = format_context_for_prompt(citations)

            # Build complete message list
            messages = create_rag_prompt(
                system_prompt=system_prompt,
                user_query=user_query,
                context=context,
                conversation_history=conversation_history or []
            )

            # Generate streaming response
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Failed to generate streaming response: {str(e)}")
            raise

    async def batch_generate_embeddings(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-small",
                input=texts,
                dimensions=1024  # Match Pinecone index dimension
            )
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {str(e)}")
            raise
