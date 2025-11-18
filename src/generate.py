#!/usr/bin/env python3
"""
Data Generation Module
Runs all analyses and generates consolidated JSON for web visualization.
"""

import json
from pathlib import Path
from collections import Counter
from preprocess import TextPreprocessor
from analyze import TextAnalyzer
from topics import TopicModeler
from sentiment import SentimentAnalyzer
from tqdm import tqdm


def load_all_texts():
    """Load and preprocess all texts"""
    processed_dir = Path('data/processed')
    txt_files = list(processed_dir.glob('*.txt'))

    if not txt_files:
        print("No texts found. Run extract.py first.")
        return None

    preprocessor = TextPreprocessor()
    all_texts = {}
    plato_texts = {}
    aristotle_texts = {}

    print("Loading texts...")
    for txt_path in tqdm(txt_files):
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        text_id = txt_path.stem
        processed = preprocessor.preprocess_for_analysis(text)
        all_texts[text_id] = processed

        # Categorize by author
        if 'Plato' in text_id:
            plato_texts[text_id] = processed
        elif 'Aristotle' in text_id or 'Artistotle' in text_id:
            aristotle_texts[text_id] = processed

    return all_texts, plato_texts, aristotle_texts


def run_all_analyses(all_texts, plato_texts, aristotle_texts):
    """Run all analysis modules"""

    analyzer = TextAnalyzer()
    modeler = TopicModeler(num_topics=8)
    sentiment_analyzer = SentimentAnalyzer()

    print("\n" + "="*60)
    print("Running Complete Analysis Pipeline")
    print("="*60)

    # 1. Basic text statistics
    print("\n1. Computing text statistics...")
    text_stats = {}
    for text_id, data in tqdm(all_texts.items(), desc="Text stats"):
        text_stats[text_id] = {
            'sentence_count': data['sentence_count'],
            'word_count': data['token_count'],
            'vocabulary_size': data['vocabulary_size'],
            'lexical_diversity': analyzer.calculate_lexical_diversity(data['tokens_lower']),
            'sentence_stats': analyzer.calculate_sentence_stats(data['sentences']),
            'word_stats': analyzer.calculate_word_stats(data['tokens_lower']),
            'top_words': analyzer.get_top_words(data['tokens_lemmatized'], n=100)
        }

    # 2. Vocabulary analysis
    print("\n2. Analyzing vocabularies...")
    author_vocab_comparison = analyzer.compare_author_vocabularies(plato_texts, aristotle_texts)

    # 3. Pairwise comparisons
    print("\n3. Computing pairwise comparisons...")
    pairwise_comparisons = {}
    text_ids = list(all_texts.keys())

    for i, id1 in enumerate(text_ids):
        for id2 in text_ids[i+1:]:
            pair_key = f"{id1}|||{id2}"  # Use ||| as separator for easy splitting
            overlap = analyzer.calculate_vocabulary_overlap(
                all_texts[id1]['tokens_lemmatized'],
                all_texts[id2]['tokens_lemmatized']
            )
            pairwise_comparisons[pair_key] = overlap

    # 4. Topic modeling
    print("\n4. Running topic modeling...")
    documents, doc_ids = modeler.prepare_documents(all_texts)
    lda_model, dictionary, corpus = modeler.train_lda_model(documents)
    topic_keywords = modeler.get_topic_keywords(lda_model, num_words=15)
    topic_distributions = modeler.get_topic_distributions(lda_model, corpus, doc_ids)
    shared_themes = modeler.identify_shared_themes(topic_distributions)

    # 5. Load pre-computed sentiment analysis
    print("\n5. Loading sentiment data...")
    sentiment_path = Path('output/sentiment.json')
    if sentiment_path.exists():
        with open(sentiment_path, 'r') as f:
            sentiment_data = json.load(f)
        all_sentiments = sentiment_data.get('individual_texts', {})
        sentiment_comparison = sentiment_data.get('author_comparison', {})
        print("   Loaded pre-computed sentiment data")
    else:
        print("   Warning: sentiment.json not found, sentiment analysis will be empty")
        all_sentiments = {}
        sentiment_comparison = {}

    # 6. Create network data for visualization
    print("\n6. Generating network data...")
    network_data = create_network_data(all_texts, pairwise_comparisons)

    return {
        'text_stats': text_stats,
        'vocabulary_analysis': author_vocab_comparison,
        'pairwise_comparisons': pairwise_comparisons,
        'topics': {
            'topic_keywords': topic_keywords,
            'document_topics': topic_distributions,
            'shared_themes': shared_themes
        },
        'sentiment': {
            'individual_texts': all_sentiments,
            'author_comparison': sentiment_comparison
        },
        'network': network_data
    }


def create_network_data(all_texts, pairwise_comparisons):
    """
    Create network graph data showing connections between texts.
    """
    nodes = []
    links = []

    # Create nodes (one per text)
    for text_id in all_texts.keys():
        author = "Plato" if "Plato" in text_id else "Aristotle"
        nodes.append({
            'id': text_id,
            'author': author,
            'label': text_id
        })

    # Create links based on vocabulary overlap
    for pair_key, overlap_data in pairwise_comparisons.items():
        id1, id2 = pair_key.split('|||')

        # Only create link if there's significant overlap
        if overlap_data['jaccard_similarity'] > 0.05:
            links.append({
                'source': id1,
                'target': id2,
                'weight': overlap_data['jaccard_similarity'],
                'shared_words': overlap_data['shared_words']
            })

    return {
        'nodes': nodes,
        'links': links
    }


def generate_all_data():
    """
    Main function to generate all analysis data.
    """
    output_dir = Path('output')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load texts
    result = load_all_texts()
    if result is None:
        return
    all_texts, plato_texts, aristotle_texts = result

    # Run all analyses
    results = run_all_analyses(all_texts, plato_texts, aristotle_texts)

    # Add metadata
    results['metadata'] = {
        'text_count': len(all_texts),
        'plato_count': len(plato_texts),
        'aristotle_count': len(aristotle_texts),
        'texts': {
            'plato': list(plato_texts.keys()),
            'aristotle': list(aristotle_texts.keys())
        }
    }

    # Save consolidated data
    output_path = output_dir / 'full_analysis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE")
    print("="*60)
    print(f"Full analysis saved to: {output_path}")
    print(f"\nData includes:")
    print(f"  - {len(all_texts)} text analyses")
    print(f"  - {len(results['pairwise_comparisons'])} pairwise comparisons")
    print(f"  - {len(results['topics']['topic_keywords'])} discovered topics")
    print(f"  - Sentiment analysis for all texts")
    print(f"  - Network graph with {len(results['network']['nodes'])} nodes and {len(results['network']['links'])} connections")
    print("\nReady for web visualization!")


if __name__ == '__main__':
    generate_all_data()
