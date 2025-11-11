"""
Upload embeddings and metadata to Pinecone.
"""
import sys
import json
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.pinecone_config import PineconeConfig


def prepare_vectors(chunks: List[Dict]) -> List[tuple]:
    """
    Prepare vectors for Pinecone upload.

    Args:
        chunks: List of chunk dictionaries with embeddings and metadata

    Returns:
        List of tuples (id, embedding, metadata)
    """
    vectors = []

    for idx, chunk in enumerate(chunks):
        # Create unique ID
        doc_name = chunk['metadata']['doc_name']
        chunk_idx = chunk['metadata']['chunk_index']
        vector_id = f"{doc_name}_{chunk_idx}"

        # Get embedding
        embedding = chunk['embedding']

        # Prepare metadata (Pinecone has some restrictions)
        metadata = {
            'doc_name': chunk['metadata']['doc_name'],
            'doc_title': chunk['metadata']['doc_title'],
            'chunk_index': chunk['metadata']['chunk_index'],
            'token_count': chunk['metadata']['token_count'],
            'text': chunk['text'][:1000],  # Truncate text to avoid size limits
        }

        # Add agent tags as separate fields for filtering
        agents = chunk['metadata']['agents']
        for agent in agents:
            metadata[f'agent_{agent}'] = True

        vectors.append((vector_id, embedding, metadata))

    return vectors


def upload_vectors(vectors: List[tuple], batch_size: int = 100):
    """
    Upload vectors to Pinecone in batches.

    Args:
        vectors: List of (id, embedding, metadata) tuples
        batch_size: Number of vectors per batch
    """
    config = PineconeConfig()
    index = config.get_index()

    print(f"Uploading {len(vectors)} vectors to Pinecone...")

    # Upload in batches
    for i in tqdm(range(0, len(vectors), batch_size), desc="Uploading batches"):
        batch = vectors[i:i + batch_size]

        # Format for Pinecone
        formatted_batch = [
            {
                'id': vec_id,
                'values': embedding,
                'metadata': metadata
            }
            for vec_id, embedding, metadata in batch
        ]

        try:
            index.upsert(vectors=formatted_batch)
        except Exception as e:
            print(f"\nError uploading batch {i // batch_size}: {str(e)}")
            raise

    print(f"✓ Uploaded {len(vectors)} vectors to index '{config.index_name}'")

    # Get updated stats
    stats = index.describe_index_stats()
    print(f"\nIndex stats:")
    print(f"  Total vectors: {stats.total_vector_count}")
    print(f"  Dimension: {stats.dimension}")


def save_manifest(chunks: List[Dict], output_path: str):
    """
    Save embeddings manifest for reference.

    Args:
        chunks: List of chunks with metadata
        output_path: Path to save manifest
    """
    manifest = {
        'total_chunks': len(chunks),
        'documents': {}
    }

    # Group by document
    for chunk in chunks:
        doc_name = chunk['metadata']['doc_name']
        if doc_name not in manifest['documents']:
            manifest['documents'][doc_name] = {
                'doc_title': chunk['metadata']['doc_title'],
                'agents': chunk['metadata']['agents'],
                'chunk_count': 0
            }
        manifest['documents'][doc_name]['chunk_count'] += 1

    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✓ Saved embeddings manifest to {output_path}")


if __name__ == "__main__":
    from scripts.chunk_documents import chunk_all_documents
    from scripts.metadata_tagger import tag_all_chunks, flatten_chunks
    from utils.embedding_handler import EmbeddingHandler

    project_root = Path(__file__).parent.parent

    # Process documents
    print("Step 1: Chunking documents...")
    raw_dir = project_root / "data" / "raw"
    output_dir = project_root / "data" / "processed"
    all_chunks = chunk_all_documents(str(raw_dir), str(output_dir))

    print("\nStep 2: Tagging chunks...")
    tagged_chunks = tag_all_chunks(all_chunks)
    flat_chunks = flatten_chunks(tagged_chunks)

    print("\nStep 3: Generating embeddings...")
    handler = EmbeddingHandler()
    embedded_chunks = handler.embed_chunks(flat_chunks)

    print("\nStep 4: Uploading to Pinecone...")
    vectors = prepare_vectors(embedded_chunks)
    upload_vectors(vectors)

    print("\nStep 5: Saving manifest...")
    manifest_path = output_dir / "embeddings_manifest.json"
    save_manifest(embedded_chunks, str(manifest_path))

    print("\n✓ Upload complete!")
