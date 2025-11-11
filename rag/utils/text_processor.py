"""
Text processing utilities for cleaning and normalizing documents.
"""
import re


def clean_text(text: str) -> str:
    """
    Clean and normalize text while preserving important structure.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned text
    """
    # Normalize whitespace but preserve paragraph breaks
    text = re.sub(r' +', ' ', text)  # Multiple spaces to single space
    text = re.sub(r'\t+', ' ', text)  # Tabs to spaces
    text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines to double newline

    # Remove zero-width characters and other invisible characters
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)

    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")

    # Remove leading/trailing whitespace from lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def extract_sections(text: str) -> list[dict]:
    """
    Extract sections from text based on headings and structure.

    Args:
        text: Document text

    Returns:
        List of dictionaries with section info
    """
    sections = []

    # Split by double newlines (paragraphs)
    paragraphs = text.split('\n\n')

    current_section = None
    section_content = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Check if this looks like a heading (short line, possibly all caps or title case)
        is_heading = (
            len(para) < 100 and
            (para.isupper() or para.istitle()) and
            not para.endswith('.')
        )

        if is_heading:
            # Save previous section
            if current_section and section_content:
                sections.append({
                    'heading': current_section,
                    'content': '\n\n'.join(section_content)
                })

            current_section = para
            section_content = []
        else:
            section_content.append(para)

    # Add final section
    if current_section and section_content:
        sections.append({
            'heading': current_section,
            'content': '\n\n'.join(section_content)
        })
    elif section_content:
        # No headings found, treat as single section
        sections.append({
            'heading': 'Main Content',
            'content': '\n\n'.join(section_content)
        })

    return sections


def preserve_structure(text: str) -> str:
    """
    Preserve important structural elements like lists and formatting.

    Args:
        text: Text to process

    Returns:
        Text with preserved structure
    """
    # Preserve bullet points and numbered lists
    text = re.sub(r'^[\s]*[-•*]\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*(\d+)\.\s+', r'\1. ', text, flags=re.MULTILINE)

    return text
