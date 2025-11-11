"""
Validation script for testing embeddings in Pinecone.
"""
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.pinecone_config import PineconeConfig
from utils.embedding_handler import EmbeddingHandler
from config.document_config import PROFESSIONAL_LEARNING, CURRICULUM_PLANNING


def test_basic_retrieval(index, handler: EmbeddingHandler):
    """
    Test basic retrieval from Pinecone.

    Args:
        index: Pinecone index
        handler: Embedding handler
    """
    print("\n" + "="*60)
    print("TEST 1: Basic Retrieval")
    print("="*60)

    test_query = "How do we build effective collaborative teams?"
    query_embedding = handler.generate_embedding(test_query)

    results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True
    )

    print(f"\nQuery: {test_query}")
    print(f"Found {len(results.matches)} results:\n")

    for i, match in enumerate(results.matches, 1):
        print(f"{i}. Score: {match.score:.4f}")
        print(f"   Document: {match.metadata.get('doc_title', 'Unknown')}")
        print(f"   Text preview: {match.metadata.get('text', '')[:150]}...")
        print()


def test_professional_learning_filter(index, handler: EmbeddingHandler):
    """
    Test filtering for Professional Learning agent.

    Args:
        index: Pinecone index
        handler: Embedding handler
    """
    print("\n" + "="*60)
    print("TEST 2: Professional Learning Agent Filter")
    print("="*60)

    test_query = "What are strategies for improving team collaboration?"
    query_embedding = handler.generate_embedding(test_query)

    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True,
        filter={f"agent_{PROFESSIONAL_LEARNING}": True}
    )

    print(f"\nQuery: {test_query}")
    print(f"Filter: agent_{PROFESSIONAL_LEARNING}")
    print(f"Found {len(results.matches)} results:\n")

    for i, match in enumerate(results.matches, 1):
        print(f"{i}. Score: {match.score:.4f}")
        print(f"   Document: {match.metadata.get('doc_title', 'Unknown')}")
        print(f"   Doc name: {match.metadata.get('doc_name', 'Unknown')}")
        print()


def test_curriculum_planning_filter(index, handler: EmbeddingHandler):
    """
    Test filtering for Curriculum Planning agent.

    Args:
        index: Pinecone index
        handler: Embedding handler
    """
    print("\n" + "="*60)
    print("TEST 3: Curriculum Planning Agent Filter")
    print("="*60)

    test_query = "How do I create learning goals for mathematics?"
    query_embedding = handler.generate_embedding(test_query)

    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True,
        filter={f"agent_{CURRICULUM_PLANNING}": True}
    )

    print(f"\nQuery: {test_query}")
    print(f"Filter: agent_{CURRICULUM_PLANNING}")
    print(f"Found {len(results.matches)} results:\n")

    for i, match in enumerate(results.matches, 1):
        print(f"{i}. Score: {match.score:.4f}")
        print(f"   Document: {match.metadata.get('doc_title', 'Unknown')}")
        print(f"   Doc name: {match.metadata.get('doc_name', 'Unknown')}")
        print()


def test_metadata_filtering(index, handler: EmbeddingHandler):
    """
    Test filtering by document name.

    Args:
        index: Pinecone index
        handler: Embedding handler
    """
    print("\n" + "="*60)
    print("TEST 4: Document-Specific Filter")
    print("="*60)

    test_query = "What are the key principles?"
    query_embedding = handler.generate_embedding(test_query)

    doc_name = "learning_by_doing.txt"
    results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True,
        filter={"doc_name": doc_name}
    )

    print(f"\nQuery: {test_query}")
    print(f"Filter: doc_name = {doc_name}")
    print(f"Found {len(results.matches)} results:\n")

    for i, match in enumerate(results.matches, 1):
        print(f"{i}. Score: {match.score:.4f}")
        print(f"   Chunk {match.metadata.get('chunk_index', '?')}")
        print(f"   Text preview: {match.metadata.get('text', '')[:150]}...")
        print()


def test_index_stats(index):
    """
    Test index statistics.

    Args:
        index: Pinecone index
    """
    print("\n" + "="*60)
    print("TEST 5: Index Statistics")
    print("="*60)

    stats = index.describe_index_stats()

    print(f"\nTotal vectors: {stats.total_vector_count}")
    print(f"Dimension: {stats.dimension}")
    print(f"Index fullness: {stats.index_fullness}")

    if hasattr(stats, 'namespaces') and stats.namespaces:
        print(f"\nNamespaces:")
        for ns, ns_stats in stats.namespaces.items():
            print(f"  {ns}: {ns_stats.vector_count} vectors")


def run_all_tests():
    """Run all validation tests."""
    print("\n" + "="*60)
    print("PINECONE EMBEDDINGS VALIDATION")
    print("="*60)

    # Initialize
    config = PineconeConfig()
    index = config.get_index()
    handler = EmbeddingHandler()

    # Run tests
    try:
        test_index_stats(index)
        test_basic_retrieval(index, handler)
        test_professional_learning_filter(index, handler)
        test_curriculum_planning_filter(index, handler)
        test_metadata_filtering(index, handler)

        print("\n" + "="*60)
        print("✓ ALL VALIDATION TESTS PASSED")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"\n✗ VALIDATION FAILED: {str(e)}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
