#!/usr/bin/env python3
"""
Topic Modeling Module
Identifies shared themes across texts using LDA.
"""

import json
from pathlib import Path
from collections import defaultdict
from gensim import corpora
from gensim.models import LdaModel
from preprocess import TextPreprocessor
from tqdm import tqdm


class TopicModeler:
    """Performs topic modeling on philosophical texts"""

    def __init__(self, num_topics=8):
        """
        Initialize topic modeler.

        Args:
            num_topics: Number of topics to extract
        """
        self.num_topics = num_topics
        self.preprocessor = TextPreprocessor()

    def prepare_documents(self, all_texts):
        """
        Prepare documents for topic modeling.

        Args:
            all_texts: Dictionary of preprocessed texts

        Returns:
            List of documents (each as list of tokens)
        """
        documents = []
        doc_ids = []

        for text_id, data in all_texts.items():
            # Use lemmatized tokens without stopwords
            documents.append(data['tokens_lemmatized'])
            doc_ids.append(text_id)

        return documents, doc_ids

    def train_lda_model(self, documents):
        """
        Train LDA topic model.

        Args:
            documents: List of token lists

        Returns:
            Trained LDA model, dictionary, and corpus
        """
        # Create dictionary
        dictionary = corpora.Dictionary(documents)

        # Filter extremes (words that appear in too many or too few documents)
        dictionary.filter_extremes(no_below=2, no_above=0.7, keep_n=1000)

        # Create corpus
        corpus = [dictionary.doc2bow(doc) for doc in documents]

        # Train LDA model
        print(f"Training LDA model with {self.num_topics} topics...")
        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=self.num_topics,
            random_state=42,
            passes=10,
            alpha='auto',
            per_word_topics=True
        )

        return lda_model, dictionary, corpus

    def get_topic_distributions(self, lda_model, corpus, doc_ids):
        """
        Get topic distribution for each document.

        Args:
            lda_model: Trained LDA model
            corpus: Document corpus
            doc_ids: Document identifiers

        Returns:
            Dictionary mapping doc_ids to topic distributions
        """
        distributions = {}

        for doc_id, doc_corpus in zip(doc_ids, corpus):
            # Get topic distribution for this document
            topic_dist = lda_model.get_document_topics(doc_corpus)

            # Convert to dictionary format
            dist_dict = {f"topic_{topic_id}": round(prob, 4) for topic_id, prob in topic_dist}

            distributions[doc_id] = dist_dict

        return distributions

    def get_topic_keywords(self, lda_model, num_words=10):
        """
        Extract top keywords for each topic.

        Args:
            lda_model: Trained LDA model
            num_words: Number of keywords per topic

        Returns:
            Dictionary of topics with keywords and weights
        """
        topics = {}

        for topic_id in range(self.num_topics):
            # Get top words for this topic
            words = lda_model.show_topic(topic_id, num_words)

            topics[f"topic_{topic_id}"] = {
                'keywords': [word for word, _ in words],
                'weights': {word: round(weight, 4) for word, weight in words}
            }

        return topics

    def identify_shared_themes(self, topic_distributions):
        """
        Identify which topics are shared across Plato and Aristotle.

        Args:
            topic_distributions: Topic distributions for all texts

        Returns:
            Analysis of shared thematic elements
        """
        plato_topics = defaultdict(list)
        aristotle_topics = defaultdict(list)

        # Aggregate topic strengths by author
        for doc_id, topics in topic_distributions.items():
            for topic, strength in topics.items():
                if 'Plato' in doc_id:
                    plato_topics[topic].append(strength)
                elif 'Aristotle' in doc_id or 'Artistotle' in doc_id:
                    aristotle_topics[topic].append(strength)

        # Calculate average strength per topic per author
        plato_avg = {topic: sum(strengths)/len(strengths) for topic, strengths in plato_topics.items()}
        aristotle_avg = {topic: sum(strengths)/len(strengths) for topic, strengths in aristotle_topics.items()}

        # Find shared themes (topics strong in both)
        shared_themes = []
        for topic in plato_avg.keys():
            if topic in aristotle_avg:
                shared_themes.append({
                    'topic': topic,
                    'plato_strength': round(plato_avg[topic], 4),
                    'aristotle_strength': round(aristotle_avg[topic], 4),
                    'total_strength': round(plato_avg[topic] + aristotle_avg[topic], 4)
                })

        # Sort by total strength
        shared_themes.sort(key=lambda x: x['total_strength'], reverse=True)

        return {
            'plato_topic_strengths': plato_avg,
            'aristotle_topic_strengths': aristotle_avg,
            'shared_themes': shared_themes
        }


def perform_topic_modeling():
    """
    Run topic modeling on all texts.
    """
    processed_dir = Path('data/processed')
    output_dir = Path('output')

    # Load all texts
    txt_files = list(processed_dir.glob('*.txt'))
    if not txt_files:
        print("No texts found. Run extract.py first.")
        return

    preprocessor = TextPreprocessor()
    modeler = TopicModeler(num_topics=8)

    print("Loading texts...")
    all_texts = {}

    for txt_path in tqdm(txt_files):
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        text_id = txt_path.stem
        processed = preprocessor.preprocess_for_analysis(text)
        all_texts[text_id] = processed

    # Prepare documents
    print("\nPreparing documents for topic modeling...")
    documents, doc_ids = modeler.prepare_documents(all_texts)

    # Train LDA model
    lda_model, dictionary, corpus = modeler.train_lda_model(documents)

    # Extract topic information
    print("\nExtracting topics...")
    topic_keywords = modeler.get_topic_keywords(lda_model, num_words=15)
    topic_distributions = modeler.get_topic_distributions(lda_model, corpus, doc_ids)
    shared_themes = modeler.identify_shared_themes(topic_distributions)

    # Compile results
    results = {
        'topics': topic_keywords,
        'document_topics': topic_distributions,
        'shared_themes': shared_themes
    }

    # Save results
    output_path = output_dir / 'topics.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\nTopic modeling complete! Results saved to {output_path}")

    # Print topic summary
    print("\n" + "="*60)
    print("DISCOVERED TOPICS")
    print("="*60)
    for topic_id, data in topic_keywords.items():
        print(f"\n{topic_id.upper()}:")
        print(f"  Keywords: {', '.join(data['keywords'][:10])}")

    print("\n" + "="*60)
    print("SHARED THEMES (Plato & Aristotle)")
    print("="*60)
    for theme in shared_themes['shared_themes'][:5]:
        topic_key = theme['topic']
        keywords = topic_keywords[topic_key]['keywords'][:5]
        print(f"\n{topic_key}: {', '.join(keywords)}")
        print(f"  Plato strength: {theme['plato_strength']:.3f}")
        print(f"  Aristotle strength: {theme['aristotle_strength']:.3f}")


if __name__ == '__main__':
    perform_topic_modeling()
