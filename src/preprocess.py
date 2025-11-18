#!/usr/bin/env python3
"""
Text Preprocessing Module
Cleans, tokenizes, and normalizes text for analysis.
"""

import re
import json
from pathlib import Path
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm


# Download required NLTK data if not already present
def ensure_nltk_data():
    """Download required NLTK data packages"""
    required = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    for package in required:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            nltk.download(package, quiet=True)


class TextPreprocessor:
    """Handles text cleaning and preprocessing"""

    def __init__(self):
        ensure_nltk_data()
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        """
        Basic text cleaning while preserving sentence structure.

        Args:
            text: Raw text string

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Fix common issues
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)  # Remove space before punctuation

        return text.strip()

    def tokenize_sentences(self, text):
        """
        Split text into sentences.

        Args:
            text: Input text

        Returns:
            List of sentences
        """
        return sent_tokenize(text)

    def tokenize_words(self, text, lowercase=True):
        """
        Tokenize text into words.

        Args:
            text: Input text
            lowercase: Convert to lowercase

        Returns:
            List of tokens
        """
        tokens = word_tokenize(text)

        if lowercase:
            tokens = [t.lower() for t in tokens]

        # Keep only alphabetic tokens (removes punctuation and numbers)
        tokens = [t for t in tokens if t.isalpha()]

        return tokens

    def remove_stopwords(self, tokens):
        """
        Remove common English stopwords.

        Args:
            tokens: List of word tokens

        Returns:
            Filtered tokens
        """
        return [t for t in tokens if t not in self.stopwords]

    def lemmatize(self, tokens):
        """
        Lemmatize tokens to their base form.

        Args:
            tokens: List of word tokens

        Returns:
            Lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(t) for t in tokens]

    def preprocess_for_analysis(self, text):
        """
        Full preprocessing pipeline for statistical analysis.

        Args:
            text: Raw text

        Returns:
            Dictionary containing various processed versions
        """
        # Clean text
        cleaned = self.clean_text(text)

        # Tokenize into sentences
        sentences = self.tokenize_sentences(cleaned)

        # Tokenize into words (preserving case for some analyses)
        tokens_original = self.tokenize_words(cleaned, lowercase=False)
        tokens_lower = self.tokenize_words(cleaned, lowercase=True)

        # Remove stopwords
        tokens_no_stop = self.remove_stopwords(tokens_lower)

        # Lemmatize
        tokens_lemmatized = self.lemmatize(tokens_no_stop)

        return {
            'cleaned_text': cleaned,
            'sentences': sentences,
            'tokens_original': tokens_original,  # For case-sensitive analysis
            'tokens_lower': tokens_lower,  # For general analysis
            'tokens_no_stopwords': tokens_no_stop,  # For content words
            'tokens_lemmatized': tokens_lemmatized,  # For vocabulary analysis
            'sentence_count': len(sentences),
            'token_count': len(tokens_lower),
            'vocabulary_size': len(set(tokens_lower)),
        }


def preprocess_all_texts():
    """
    Preprocess all extracted texts and save preprocessed versions.
    """
    processed_dir = Path('data/processed')
    output_dir = Path('output')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all .txt files
    txt_files = list(processed_dir.glob('*.txt'))

    if not txt_files:
        print(f"No .txt files found in {processed_dir}")
        print("Run extract.py first to extract text from .docx files")
        return

    preprocessor = TextPreprocessor()
    all_data = {}

    print(f"Preprocessing {len(txt_files)} texts...")

    for txt_path in tqdm(txt_files, desc="Preprocessing"):
        # Read text
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Preprocess
        processed = preprocessor.preprocess_for_analysis(text)

        # Store with clean filename
        text_id = txt_path.stem  # e.g., "Aristotle Gov"
        all_data[text_id] = processed

        # Print stats
        print(f"\n{text_id}:")
        print(f"  Sentences: {processed['sentence_count']:,}")
        print(f"  Words: {processed['token_count']:,}")
        print(f"  Unique words: {processed['vocabulary_size']:,}")
        print(f"  Lexical diversity: {processed['vocabulary_size']/processed['token_count']:.3f}")

    # Save preprocessed data (excluding full token lists for file size)
    output_data = {}
    for text_id, data in all_data.items():
        output_data[text_id] = {
            'sentence_count': data['sentence_count'],
            'token_count': data['token_count'],
            'vocabulary_size': data['vocabulary_size'],
            'lexical_diversity': data['vocabulary_size'] / data['token_count'],
            # Save top 100 most common words
            'top_words': dict(Counter(data['tokens_lemmatized']).most_common(100)),
        }

    output_path = output_dir / 'preprocessed_stats.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nPreprocessing complete!")
    print(f"Stats saved to {output_path}")

    return all_data


if __name__ == '__main__':
    preprocess_all_texts()
