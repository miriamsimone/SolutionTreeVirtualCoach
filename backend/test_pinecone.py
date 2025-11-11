"""
Quick test script to check Pinecone index contents.
"""
import asyncio
import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.config import get_settings
from app.services.pinecone_service import PineconeService
from app.services.openai_service import OpenAIService


async def test_pinecone():
    """Test Pinecone connection and query."""
    print("Testing Pinecone connection...")
    print("=" * 60)

    settings = get_settings()
    pinecone_service = PineconeService(settings)
    openai_service = OpenAIService(settings)

    # Get index stats
    try:
        stats = pinecone_service.get_index_stats()
        print(f"✓ Connected to Pinecone index: {settings.pinecone_index_name}")
        print(f"  Dimension: {stats['dimension']}")
        print(f"  Total vectors: {stats['total_vector_count']}")
        print(f"  Namespaces: {stats.get('namespaces', {})}")
        print()
    except Exception as e:
        print(f"✗ Failed to get index stats: {e}")
        return

    # Check if index is empty
    if stats['total_vector_count'] == 0:
        print("⚠️  Pinecone index is EMPTY - no documents ingested yet!")
        print("   You need to ingest documents before the chat will work.")
        return

    # Try a test query
    print("Testing query with sample text...")
    try:
        test_query = "How can we improve team collaboration in PLCs?"
        print(f"Query: '{test_query}'")

        # Generate embedding
        embedding = await openai_service.get_embedding(test_query)
        print(f"✓ Generated embedding with {len(embedding)} dimensions")

        # Query without filter
        print("\nQuerying Pinecone (no metadata filter)...")
        citations = await pinecone_service.query_documents(
            query_embedding=embedding,
            metadata_filter=None,
            top_k=3
        )

        print(f"✓ Found {len(citations)} documents")

        if citations:
            print("\nTop 3 results:")
            for i, cite in enumerate(citations, 1):
                print(f"\n  [{i}] {cite.source_title}")
                print(f"      Score: {cite.relevance_score:.4f}")
                if cite.page_number:
                    print(f"      Page: {cite.page_number}")
                preview = cite.chunk_text[:100] + "..." if len(cite.chunk_text) > 100 else cite.chunk_text
                print(f"      Text: {preview}")
        else:
            print("⚠️  Query returned 0 results even without filters")
            print("   This might be a dimension mismatch or empty index")

    except Exception as e:
        print(f"✗ Query failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_pinecone())
