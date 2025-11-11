"""
Main ingestion script to orchestrate the full RAG pipeline.
Runs chunking, tagging, embedding, and upload to Pinecone.
"""
import sys
import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.chunk_documents import chunk_all_documents
from scripts.metadata_tagger import tag_all_chunks, flatten_chunks
from utils.embedding_handler import EmbeddingHandler
from scripts.upload_to_pinecone import prepare_vectors, upload_vectors, save_manifest


def run_ingestion_pipeline(raw_dir: str, output_dir: str, skip_upload: bool = False):
    """
    Run the complete ingestion pipeline.

    Args:
        raw_dir: Directory containing raw documents
        output_dir: Directory for processed output
        skip_upload: If True, skip uploading to Pinecone (for testing)
    """
    print("\n" + "="*60)
    print("RAG INGESTION PIPELINE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Step 1: Chunk documents
    print("STEP 1: Chunking documents")
    print("-" * 60)
    all_chunks = chunk_all_documents(raw_dir, output_dir)
    total_chunks = sum(len(chunks) for chunks in all_chunks.values())
    print(f"✓ Created {total_chunks} chunks from {len(all_chunks)} documents\n")

    # Step 2: Tag with metadata
    print("STEP 2: Tagging chunks with metadata")
    print("-" * 60)
    tagged_chunks = tag_all_chunks(all_chunks)
    flat_chunks = flatten_chunks(tagged_chunks)
    print(f"✓ Tagged {len(flat_chunks)} chunks\n")

    # Step 3: Generate embeddings
    print("STEP 3: Generating embeddings")
    print("-" * 60)
    handler = EmbeddingHandler()
    embedded_chunks = handler.embed_chunks(flat_chunks)
    print()

    # Step 4: Upload to Pinecone (optional)
    if not skip_upload:
        print("STEP 4: Uploading to Pinecone")
        print("-" * 60)
        vectors = prepare_vectors(embedded_chunks)
        upload_vectors(vectors)
        print()
    else:
        print("STEP 4: Skipping Pinecone upload (skip_upload=True)\n")

    # Step 5: Save manifest
    print("STEP 5: Saving embeddings manifest")
    print("-" * 60)
    manifest_path = Path(output_dir) / "embeddings_manifest.json"
    save_manifest(embedded_chunks, str(manifest_path))
    print()

    # Summary
    print("="*60)
    print("INGESTION COMPLETE")
    print("="*60)
    print(f"Documents processed: {len(all_chunks)}")
    print(f"Total chunks: {len(flat_chunks)}")
    print(f"Embeddings generated: {len(embedded_chunks)}")

    if not skip_upload:
        print(f"Vectors uploaded: {len(embedded_chunks)}")

    print(f"Manifest saved: {manifest_path}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

    return embedded_chunks


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="RAG ingestion pipeline")
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        help="Skip uploading to Pinecone (for testing)"
    )
    parser.add_argument(
        "--raw-dir",
        default=None,
        help="Directory containing raw documents"
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for processed output"
    )

    args = parser.parse_args()

    # Set default paths
    project_root = Path(__file__).parent.parent
    raw_dir = args.raw_dir or str(project_root / "data" / "raw")
    output_dir = args.output_dir or str(project_root / "data" / "processed")

    try:
        run_ingestion_pipeline(raw_dir, output_dir, args.skip_upload)
        return 0
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
