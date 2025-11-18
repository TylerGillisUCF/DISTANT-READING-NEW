#!/usr/bin/env python3
"""
Core Analysis Module
Performs statistical and stylistic analysis on preprocessed texts.
"""

import json
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict
from preprocess import TextPreprocessor
from tqdm import tqdm


class TextAnalyzer:
    """Performs various textual analyses"""

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def calculate_lexical_diversity(self, tokens):
        """
        Calculate Type-Token Ratio (TTR) and related metrics.

        Args:
            tokens: List of word tokens

        Returns:
            Dictionary of diversity metrics
        """
        total_tokens = len(tokens)
        unique_tokens = len(set(tokens))

        if total_tokens == 0:
            return {'ttr': 0, 'unique_words': 0, 'total_words': 0}

        ttr = unique_tokens / total_tokens

        # Calculate MTLD (Measure of Textual Lexical Diversity) - simplified version
        # Higher MTLD indicates more diverse vocabulary
        mtld = self._calculate_mtld(tokens)

        return {
            'ttr': round(ttr, 4),
            'unique_words': unique_tokens,
            'total_words': total_tokens,
            'mtld': round(mtld, 2)
        }

    def _calculate_mtld(self, tokens, threshold=0.72):
        """
        Calculate MTLD (simplified version).
        Measures how many words on average before dropping below a TTR threshold.
        """
        if len(tokens) < 50:
            return 0

        factors = 0
        start = 0
        token_types = set()

        for i, token in enumerate(tokens):
            token_types.add(token)
            ttr = len(token_types) / (i - start + 1)

            if ttr < threshold:
                factors += 1
                start = i + 1
                token_types = set()

        if factors == 0:
            return len(tokens)

        return len(tokens) / factors

    def calculate_sentence_stats(self, sentences):
        """
        Calculate sentence-level statistics.

        Args:
            sentences: List of sentences

        Returns:
            Dictionary of sentence metrics
        """
        if not sentences:
            return {}

        sentence_lengths = [len(s.split()) for s in sentences]

        return {
            'sentence_count': len(sentences),
            'avg_sentence_length': round(np.mean(sentence_lengths), 2),
            'median_sentence_length': round(np.median(sentence_lengths), 2),
            'min_sentence_length': min(sentence_lengths),
            'max_sentence_length': max(sentence_lengths),
            'std_sentence_length': round(np.std(sentence_lengths), 2)
        }

    def calculate_word_stats(self, tokens):
        """
        Calculate word-level statistics.

        Args:
            tokens: List of word tokens

        Returns:
            Dictionary of word metrics
        """
        if not tokens:
            return {}

        word_lengths = [len(word) for word in tokens]

        return {
            'avg_word_length': round(np.mean(word_lengths), 2),
            'median_word_length': round(np.median(word_lengths), 2),
            'long_words': sum(1 for w in word_lengths if w > 6),  # Complex words
            'long_word_ratio': round(sum(1 for w in word_lengths if w > 6) / len(tokens), 4)
        }

    def calculate_vocabulary_overlap(self, tokens1, tokens2):
        """
        Calculate vocabulary overlap between two texts.

        Args:
            tokens1: Tokens from first text
            tokens2: Tokens from second text

        Returns:
            Dictionary with overlap metrics
        """
        vocab1 = set(tokens1)
        vocab2 = set(tokens2)

        shared = vocab1 & vocab2
        unique1 = vocab1 - vocab2
        unique2 = vocab2 - vocab1

        # Jaccard similarity
        jaccard = len(shared) / len(vocab1 | vocab2) if (vocab1 | vocab2) else 0

        return {
            'shared_words': len(shared),
            'unique_to_first': len(unique1),
            'unique_to_second': len(unique2),
            'jaccard_similarity': round(jaccard, 4),
            'overlap_percentage_first': round(len(shared) / len(vocab1) * 100, 2) if vocab1 else 0,
            'overlap_percentage_second': round(len(shared) / len(vocab2) * 100, 2) if vocab2 else 0,
            'shared_words_list': sorted(list(shared))[:100]  # Top 100 for display
        }

    def get_top_words(self, tokens, n=50, exclude_common=True):
        """
        Get most frequent words.

        Args:
            tokens: List of tokens
            n: Number of top words to return
            exclude_common: Whether to exclude stopwords

        Returns:
            List of (word, count) tuples
        """
        if exclude_common:
            # Filter out very common words that might not be meaningful
            common = {'said', 'one', 'upon', 'like', 'would', 'also', 'may', 'must', 'every', 'much'}
            tokens = [t for t in tokens if t not in common]

        counter = Counter(tokens)
        return counter.most_common(n)

    def compare_author_vocabularies(self, plato_texts, aristotle_texts):
        """
        Compare vocabularies between Plato and Aristotle.

        Args:
            plato_texts: Dictionary of Plato's processed texts
            aristotle_texts: Dictionary of Aristotle's processed texts

        Returns:
            Analysis of teacher-student vocabulary relationship
        """
        # Combine all tokens for each author
        plato_tokens = []
        for text_data in plato_texts.values():
            plato_tokens.extend(text_data['tokens_lemmatized'])

        aristotle_tokens = []
        for text_data in aristotle_texts.values():
            aristotle_tokens.extend(text_data['tokens_lemmatized'])

        # Get unique vocabularies
        plato_vocab = set(plato_tokens)
        aristotle_vocab = set(aristotle_tokens)

        # Calculate overlap
        shared = plato_vocab & aristotle_vocab
        plato_unique = plato_vocab - aristotle_vocab
        aristotle_unique = aristotle_vocab - plato_vocab

        # Get frequency of shared terms
        plato_freq = Counter(plato_tokens)
        aristotle_freq = Counter(aristotle_tokens)

        shared_freq = {
            word: {
                'plato_count': plato_freq[word],
                'aristotle_count': aristotle_freq[word],
                'total': plato_freq[word] + aristotle_freq[word]
            }
            for word in shared
        }

        # Sort by total frequency
        top_shared = sorted(shared_freq.items(), key=lambda x: x[1]['total'], reverse=True)[:100]

        return {
            'plato_vocabulary_size': len(plato_vocab),
            'aristotle_vocabulary_size': len(aristotle_vocab),
            'shared_vocabulary': len(shared),
            'plato_unique': len(plato_unique),
            'aristotle_unique': len(aristotle_unique),
            'overlap_percentage': round(len(shared) / len(plato_vocab | aristotle_vocab) * 100, 2),
            'aristotle_uses_plato': round(len(shared) / len(plato_vocab) * 100, 2),
            'top_shared_words': [{
                'word': word,
                'plato_count': data['plato_count'],
                'aristotle_count': data['aristotle_count']
            } for word, data in top_shared[:50]],
            'top_plato_unique': Counter([t for t in plato_tokens if t in plato_unique]).most_common(30),
            'top_aristotle_unique': Counter([t for t in aristotle_tokens if t in aristotle_unique]).most_common(30)
        }


def analyze_all_texts():
    """
    Run complete analysis on all texts.
    """
    processed_dir = Path('data/processed')
    output_dir = Path('output')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load all texts
    txt_files = list(processed_dir.glob('*.txt'))
    if not txt_files:
        print("No texts found. Run extract.py first.")
        return

    preprocessor = TextPreprocessor()
    analyzer = TextAnalyzer()

    print("Loading and preprocessing texts...")
    all_texts = {}
    plato_texts = {}
    aristotle_texts = {}

    for txt_path in tqdm(txt_files):
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        text_id = txt_path.stem
        processed = preprocessor.preprocess_for_analysis(text)
        all_texts[text_id] = processed

        # Categorize by author
        if 'Plato' in text_id:
            plato_texts[text_id] = processed
        elif 'Aristotle' in text_id or 'Artistotle' in text_id:  # Handle typo
            aristotle_texts[text_id] = processed

    print(f"\nAnalyzing {len(all_texts)} texts...")

    # Analyze each text individually
    results = {}
    for text_id, data in tqdm(all_texts.items(), desc="Individual analysis"):
        results[text_id] = {
            'basic_stats': {
                'sentence_count': data['sentence_count'],
                'word_count': data['token_count'],
                'vocabulary_size': data['vocabulary_size']
            },
            'lexical_diversity': analyzer.calculate_lexical_diversity(data['tokens_lower']),
            'sentence_stats': analyzer.calculate_sentence_stats(data['sentences']),
            'word_stats': analyzer.calculate_word_stats(data['tokens_lower']),
            'top_words': analyzer.get_top_words(data['tokens_lemmatized'], n=50)
        }

    # Compare Plato and Aristotle
    print("\nComparing Plato and Aristotle vocabularies...")
    author_comparison = analyzer.compare_author_vocabularies(plato_texts, aristotle_texts)

    # Pairwise comparisons between all texts
    print("\nCalculating pairwise vocabulary overlaps...")
    pairwise_overlaps = {}
    text_ids = list(all_texts.keys())

    for i, id1 in enumerate(text_ids):
        for id2 in text_ids[i+1:]:
            pair_key = f"{id1} vs {id2}"
            overlap = analyzer.calculate_vocabulary_overlap(
                all_texts[id1]['tokens_lemmatized'],
                all_texts[id2]['tokens_lemmatized']
            )
            pairwise_overlaps[pair_key] = overlap

    # Save results
    output = {
        'individual_texts': results,
        'plato_vs_aristotle': author_comparison,
        'pairwise_comparisons': pairwise_overlaps
    }

    output_path = output_dir / 'analysis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"\nAnalysis complete! Results saved to {output_path}")

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY: Plato vs Aristotle")
    print("="*60)
    print(f"Plato's vocabulary: {author_comparison['plato_vocabulary_size']:,} unique words")
    print(f"Aristotle's vocabulary: {author_comparison['aristotle_vocabulary_size']:,} unique words")
    print(f"Shared vocabulary: {author_comparison['shared_vocabulary']:,} words")
    print(f"Overlap: {author_comparison['overlap_percentage']}%")
    print(f"\nTop shared philosophical terms:")
    for item in author_comparison['top_shared_words'][:10]:
        print(f"  {item['word']}: Plato used {item['plato_count']}x, Aristotle used {item['aristotle_count']}x")


if __name__ == '__main__':
    analyze_all_texts()
