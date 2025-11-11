"""
Document chunking script for creating semantic chunks from raw text documents.
"""
import os
import sys
from pathlib import Path
import tiktoken

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.document_config import CHUNK_SIZE, CHUNK_OVERLAP
from utils.text_processor import clean_text, preserve_structure


def count_tokens(text: str, model: str = "text-embedding-3-small") -> int:
    """
    Count tokens in text using tiktoken.

    Args:
        text: Text to count tokens for
        model: Model name for tokenizer

    Returns:
        Token count
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into chunks with overlap, respecting sentence boundaries.

    Args:
        text: Text to chunk
        chunk_size: Target chunk size in tokens
        overlap: Overlap size in tokens

    Returns:
        List of text chunks
    """
    # Split into sentences (rough approximation)
    sentences = []
    current = []

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            if current:
                sentences.append('\n'.join(current))
                current = []
            continue

        # Split on sentence boundaries
        parts = line.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
        for part in parts:
            part = part.strip()
            if part:
                current.append(part)

    if current:
        sentences.append('\n'.join(current))

    # Build chunks
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)

        # If single sentence exceeds chunk size, split it
        if sentence_tokens > chunk_size:
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_tokens = 0

            # Split long sentence by words
            words = sentence.split()
            temp_chunk = []
            temp_tokens = 0

            for word in words:
                word_tokens = count_tokens(word)
                if temp_tokens + word_tokens > chunk_size:
                    if temp_chunk:
                        chunks.append(' '.join(temp_chunk))
                    temp_chunk = [word]
                    temp_tokens = word_tokens
                else:
                    temp_chunk.append(word)
                    temp_tokens += word_tokens

            if temp_chunk:
                chunks.append(' '.join(temp_chunk))
            continue

        # Check if adding this sentence exceeds chunk size
        if current_tokens + sentence_tokens > chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))

            # Add overlap from previous chunk
            overlap_chunk = []
            overlap_tokens = 0
            for sent in reversed(current_chunk):
                sent_tokens = count_tokens(sent)
                if overlap_tokens + sent_tokens <= overlap:
                    overlap_chunk.insert(0, sent)
                    overlap_tokens += sent_tokens
                else:
                    break

            current_chunk = overlap_chunk
            current_tokens = overlap_tokens

        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    # Add final chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks


def chunk_document(file_path: str, output_dir: str) -> list[dict]:
    """
    Read and chunk a single document.

    Args:
        file_path: Path to document
        output_dir: Directory for processed output

    Returns:
        List of chunk dictionaries with metadata
    """
    file_name = os.path.basename(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Clean and process text
    text = clean_text(raw_text)
    text = preserve_structure(text)

    # Chunk the text
    chunks = chunk_text(text)

    # Create chunk metadata
    chunk_data = []
    for idx, chunk_content in enumerate(chunks):
        chunk_data.append({
            'chunk_index': idx,
            'text': chunk_content,
            'doc_name': file_name,
            'token_count': count_tokens(chunk_content)
        })

    print(f"✓ {file_name}: {len(chunks)} chunks created")

    return chunk_data


def chunk_all_documents(raw_dir: str, output_dir: str) -> dict:
    """
    Chunk all documents in raw directory.

    Args:
        raw_dir: Directory containing raw documents
        output_dir: Directory for processed output

    Returns:
        Dictionary mapping file names to chunk data
    """
    os.makedirs(output_dir, exist_ok=True)

    all_chunks = {}

    for file_name in os.listdir(raw_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(raw_dir, file_name)
            chunks = chunk_document(file_path, output_dir)
            all_chunks[file_name] = chunks

    return all_chunks


if __name__ == "__main__":
    # Example usage
    project_root = Path(__file__).parent.parent
    raw_dir = project_root / "data" / "raw"
    output_dir = project_root / "data" / "processed"

    print("Chunking documents...")
    all_chunks = chunk_all_documents(str(raw_dir), str(output_dir))

    total_chunks = sum(len(chunks) for chunks in all_chunks.values())
    print(f"\n✓ Total chunks created: {total_chunks}")
