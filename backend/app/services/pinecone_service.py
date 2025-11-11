"""
Pinecone vector database service for document retrieval.
"""
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
import logging
from app.config import Settings
from app.models.schemas import Citation
import uuid

logger = logging.getLogger(__name__)


class PineconeService:
    """Service for interacting with Pinecone vector database."""

    def __init__(self, settings: Settings):
        """
        Initialize Pinecone service.

        Args:
            settings: Application settings containing Pinecone configuration
        """
        self.settings = settings
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name
        self.top_k = settings.pinecone_top_k
        self._index = None

    def get_index(self):
        """Get or create Pinecone index connection."""
        if self._index is None:
            try:
                self._index = self.pc.Index(self.index_name)
                logger.info(f"Connected to Pinecone index: {self.index_name}")
            except Exception as e:
                logger.error(f"Failed to connect to Pinecone index: {str(e)}")
                raise
        return self._index

    async def query_documents(
        self,
        query_embedding: List[float],
        metadata_filter: Optional[Dict[str, Any]] = None,
        top_k: Optional[int] = None
    ) -> List[Citation]:
        """
        Query Pinecone for similar documents with optional metadata filtering.

        Args:
            query_embedding: Vector embedding of the query
            metadata_filter: Optional metadata filter for agent-specific documents
            top_k: Number of results to return (defaults to settings value)

        Returns:
            List of Citation objects with retrieved document information
        """
        try:
            index = self.get_index()
            k = top_k or self.top_k

            # Build query parameters
            query_params = {
                "vector": query_embedding,
                "top_k": k,
                "include_metadata": True
            }

            # Add metadata filter if provided
            if metadata_filter:
                query_params["filter"] = metadata_filter
                logger.debug(f"Applying metadata filter: {metadata_filter}")

            # Execute query
            results = index.query(**query_params)

            # Convert results to Citation objects
            citations = []
            for i, match in enumerate(results.matches):
                metadata = match.metadata or {}

                citation = Citation(
                    id=f"cite_{i+1}",
                    source_title=metadata.get("doc_title", metadata.get("source_title", metadata.get("title", "Unknown Source"))),
                    page_number=metadata.get("page_number", metadata.get("page", metadata.get("chunk_index"))),
                    chunk_text=metadata.get("text", metadata.get("content", metadata.get("chunk_text", ""))),
                    relevance_score=float(match.score)
                )
                citations.append(citation)

            logger.info(f"Retrieved {len(citations)} documents from Pinecone")
            return citations

        except Exception as e:
            logger.error(f"Pinecone query failed: {str(e)}")
            raise

    async def upsert_documents(
        self,
        vectors: List[tuple],
        namespace: str = ""
    ) -> Dict[str, int]:
        """
        Insert or update vectors in Pinecone.

        Args:
            vectors: List of (id, embedding, metadata) tuples
            namespace: Optional namespace for organization

        Returns:
            Dict with upsert statistics
        """
        try:
            index = self.get_index()
            response = index.upsert(vectors=vectors, namespace=namespace)
            logger.info(f"Upserted {response.upserted_count} vectors to Pinecone")
            return {"upserted_count": response.upserted_count}
        except Exception as e:
            logger.error(f"Pinecone upsert failed: {str(e)}")
            raise

    async def delete_by_metadata(
        self,
        metadata_filter: Dict[str, Any],
        namespace: str = ""
    ) -> None:
        """
        Delete vectors matching metadata filter.

        Args:
            metadata_filter: Metadata filter for deletion
            namespace: Optional namespace
        """
        try:
            index = self.get_index()
            index.delete(filter=metadata_filter, namespace=namespace)
            logger.info(f"Deleted vectors matching filter: {metadata_filter}")
        except Exception as e:
            logger.error(f"Pinecone delete failed: {str(e)}")
            raise

    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the Pinecone index."""
        try:
            index = self.get_index()
            stats = index.describe_index_stats()
            return {
                "dimension": stats.dimension,
                "total_vector_count": stats.total_vector_count,
                "namespaces": stats.namespaces
            }
        except Exception as e:
            logger.error(f"Failed to get index stats: {str(e)}")
            raise
