#!/usr/bin/env python3
"""
Text Extraction Module
Extracts text content from Word (.docx) documents.
"""

import os
from pathlib import Path
from docx import Document
from tqdm import tqdm


def extract_text_from_docx(docx_path):
    """
    Extract all text from a .docx file.

    Args:
        docx_path: Path to the .docx file

    Returns:
        Extracted text as a string
    """
    doc = Document(docx_path)
    full_text = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:  # Only add non-empty paragraphs
            full_text.append(text)

    return '\n\n'.join(full_text)


def extract_all_texts():
    """
    Extract text from all .docx files in data/raw/ and save to data/processed/
    """
    # Setup paths
    raw_dir = Path('data/raw')
    processed_dir = Path('data/processed')
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Get all .docx files
    docx_files = list(raw_dir.glob('*.docx'))

    if not docx_files:
        print(f"No .docx files found in {raw_dir}")
        return

    print(f"Found {len(docx_files)} documents to extract")

    # Extract each document
    for docx_path in tqdm(docx_files, desc="Extracting texts"):
        # Create output filename (replace .docx with .txt)
        output_filename = docx_path.stem + '.txt'
        output_path = processed_dir / output_filename

        # Extract text
        text = extract_text_from_docx(docx_path)

        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        # Print stats
        word_count = len(text.split())
        char_count = len(text)
        print(f"  {docx_path.name}: {word_count:,} words, {char_count:,} characters")

    print(f"\nExtraction complete! Texts saved to {processed_dir}")


if __name__ == '__main__':
    extract_all_texts()
