"""
Metadata tagging script for adding agent affinity and document metadata to chunks.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.document_config import DOCUMENT_AGENT_MAPPING, DOCUMENT_TITLES


def add_metadata(chunk_data: dict, file_name: str) -> dict:
    """
    Add agent affinity and document metadata to a chunk.

    Args:
        chunk_data: Chunk dictionary with text and basic metadata
        file_name: Name of source file

    Returns:
        Chunk with added metadata
    """
    # Get agent affinity
    agents = DOCUMENT_AGENT_MAPPING.get(file_name, [])

    # Get friendly document title
    doc_title = DOCUMENT_TITLES.get(file_name, file_name)

    # Add metadata
    chunk_data['metadata'] = {
        'doc_name': file_name,
        'doc_title': doc_title,
        'agents': agents,
        'chunk_index': chunk_data['chunk_index'],
        'token_count': chunk_data['token_count']
    }

    return chunk_data


def tag_all_chunks(all_chunks: dict) -> dict:
    """
    Add metadata to all chunks.

    Args:
        all_chunks: Dictionary mapping file names to chunk lists

    Returns:
        Dictionary with metadata-tagged chunks
    """
    tagged_chunks = {}

    for file_name, chunks in all_chunks.items():
        tagged = []
        for chunk in chunks:
            tagged_chunk = add_metadata(chunk, file_name)
            tagged.append(tagged_chunk)

        tagged_chunks[file_name] = tagged
        print(f"✓ Tagged {len(tagged)} chunks from {file_name}")

    return tagged_chunks


def flatten_chunks(tagged_chunks: dict) -> list[dict]:
    """
    Flatten nested chunk structure into a single list.

    Args:
        tagged_chunks: Dictionary mapping file names to chunk lists

    Returns:
        Flat list of all chunks with metadata
    """
    all_chunks = []

    for file_name, chunks in tagged_chunks.items():
        all_chunks.extend(chunks)

    return all_chunks


if __name__ == "__main__":
    # Example usage
    from scripts.chunk_documents import chunk_all_documents

    project_root = Path(__file__).parent.parent
    raw_dir = project_root / "data" / "raw"
    output_dir = project_root / "data" / "processed"

    print("Chunking documents...")
    all_chunks = chunk_all_documents(str(raw_dir), str(output_dir))

    print("\nTagging chunks with metadata...")
    tagged_chunks = tag_all_chunks(all_chunks)

    flat_chunks = flatten_chunks(tagged_chunks)
    print(f"\n✓ Total tagged chunks: {len(flat_chunks)}")
