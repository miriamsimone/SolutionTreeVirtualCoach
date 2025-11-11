"""
Pinecone configuration and connection management.
"""
import os
from pinecone import Pinecone, ServerlessSpec


class PineconeConfig:
    """Configuration and connection handler for Pinecone."""

    def __init__(self, api_key: str = None, index_name: str = None):
        """
        Initialize Pinecone configuration.

        Args:
            api_key: Pinecone API key (defaults to env var)
            index_name: Name of Pinecone index (defaults to env var)
        """
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.index_name = index_name or os.getenv("PINECONE_INDEX_NAME")

        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment")
        if not self.index_name:
            raise ValueError("PINECONE_INDEX_NAME not found in environment")

        # Initialize Pinecone client
        self.pc = Pinecone(api_key=self.api_key)

    def get_index(self):
        """
        Get or create Pinecone index.

        Returns:
            Pinecone index object
        """
        # Check if index exists
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            print(f"Index '{self.index_name}' not found. Creating...")
            self.pc.create_index(
                name=self.index_name,
                dimension=1024,  # text-embedding-3-small with dimensions=1024
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print(f"✓ Created index '{self.index_name}'")
        else:
            print(f"✓ Using existing index '{self.index_name}'")

        return self.pc.Index(self.index_name)

    def delete_index(self):
        """Delete the Pinecone index (use with caution)."""
        self.pc.delete_index(self.index_name)
        print(f"✓ Deleted index '{self.index_name}'")

    def get_index_stats(self):
        """Get statistics about the index."""
        index = self.get_index()
        stats = index.describe_index_stats()
        return stats


if __name__ == "__main__":
    # Test Pinecone connection
    config = PineconeConfig()
    index = config.get_index()

    print(f"\nIndex: {config.index_name}")
    print(f"Stats: {config.get_index_stats()}")
