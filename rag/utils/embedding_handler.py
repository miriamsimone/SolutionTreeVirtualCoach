"""
Embedding generation handler using OpenAI API.
"""
import os
import time
from typing import List
from openai import OpenAI
from tqdm import tqdm


class EmbeddingHandler:
    """Handler for generating embeddings using OpenAI API."""

    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small", dimensions: int = 1024):
        """
        Initialize embedding handler.

        Args:
            api_key: OpenAI API key (defaults to env var)
            model: Embedding model to use
            dimensions: Target dimension for embeddings (1024 for plc-coach index)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.dimensions = dimensions
        self.client = OpenAI(api_key=self.api_key)

    def generate_embedding(self, text: str, retry_count: int = 3) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed
            retry_count: Number of retries on failure

        Returns:
            Embedding vector
        """
        for attempt in range(retry_count):
            try:
                response = self.client.embeddings.create(
                    input=text,
                    model=self.model,
                    dimensions=self.dimensions
                )
                return response.data[0].embedding

            except Exception as e:
                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"  Retry {attempt + 1}/{retry_count} after {wait_time}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to generate embedding after {retry_count} attempts: {str(e)}")

    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts per batch

        Returns:
            List of embedding vectors
        """
        embeddings = []

        # Process in batches with progress bar
        for i in tqdm(range(0, len(texts), batch_size), desc="Generating embeddings"):
            batch = texts[i:i + batch_size]

            try:
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model,
                    dimensions=self.dimensions
                )

                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)

            except Exception as e:
                print(f"\nError in batch {i // batch_size}: {str(e)}")
                # Fall back to individual processing for this batch
                print("Falling back to individual processing...")
                for text in batch:
                    embedding = self.generate_embedding(text)
                    embeddings.append(embedding)

            # Small delay to avoid rate limiting
            time.sleep(0.1)

        return embeddings

    def embed_chunks(self, chunks: List[dict]) -> List[dict]:
        """
        Add embeddings to chunk dictionaries.

        Args:
            chunks: List of chunk dictionaries with 'text' field

        Returns:
            Chunks with added 'embedding' field
        """
        print(f"Generating embeddings for {len(chunks)} chunks...")

        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.generate_embeddings_batch(texts)

        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding

        print(f"✓ Generated {len(embeddings)} embeddings")

        return chunks


if __name__ == "__main__":
    # Test embedding generation
    handler = EmbeddingHandler()

    test_text = "This is a test sentence for embedding generation."
    embedding = handler.generate_embedding(test_text)

    print(f"Generated embedding with dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
