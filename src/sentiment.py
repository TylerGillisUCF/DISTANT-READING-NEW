#!/usr/bin/env python3
"""
Sentiment Analysis Module
Analyzes emotional tone and sentiment in philosophical texts.
"""

import json
from pathlib import Path
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from preprocess import TextPreprocessor
from tqdm import tqdm


class SentimentAnalyzer:
    """Analyzes sentiment and emotional tone"""

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.preprocessor = TextPreprocessor()

    def analyze_with_vader(self, text):
        """
        Analyze sentiment using VADER (Valence Aware Dictionary).
        Good for social media and general text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary of VADER scores
        """
        scores = self.vader.polarity_scores(text)
        return {
            'positive': round(scores['pos'], 4),
            'negative': round(scores['neg'], 4),
            'neutral': round(scores['neu'], 4),
            'compound': round(scores['compound'], 4)  # Overall score from -1 to 1
        }

    def analyze_with_textblob(self, text):
        """
        Analyze sentiment using TextBlob.
        Provides polarity and subjectivity.

        Args:
            text: Text to analyze

        Returns:
            Dictionary of TextBlob scores
        """
        blob = TextBlob(text)

        return {
            'polarity': round(blob.sentiment.polarity, 4),  # -1 to 1
            'subjectivity': round(blob.sentiment.subjectivity, 4)  # 0 to 1
        }

    def analyze_sentence_sentiment_distribution(self, sentences):
        """
        Analyze sentiment distribution across sentences (sampled for performance).

        Args:
            sentences: List of sentences

        Returns:
            Dictionary with sentiment distribution statistics
        """
        if not sentences:
            return {}

        # Sample sentences for performance (analyze every 10th sentence or max 500)
        import random
        if len(sentences) > 500:
            sample_size = 500
            sampled_sentences = random.sample(sentences, sample_size)
        elif len(sentences) > 50:
            sampled_sentences = sentences[::max(1, len(sentences)//100)]  # Sample ~100 sentences
        else:
            sampled_sentences = sentences

        polarities = []
        subjectivities = []

        for sent in sampled_sentences:
            blob = TextBlob(sent)
            polarities.append(blob.sentiment.polarity)
            subjectivities.append(blob.sentiment.subjectivity)

        # Categorize polarities
        positive_count = sum(1 for p in polarities if p > 0.1)
        negative_count = sum(1 for p in polarities if p < -0.1)
        neutral_count = sum(1 for p in polarities if -0.1 <= p <= 0.1)

        return {
            'avg_polarity': round(np.mean(polarities), 4),
            'std_polarity': round(np.std(polarities), 4),
            'avg_subjectivity': round(np.mean(subjectivities), 4),
            'std_subjectivity': round(np.std(subjectivities), 4),
            'positive_sentences': positive_count,
            'negative_sentences': negative_count,
            'neutral_sentences': neutral_count,
            'positive_ratio': round(positive_count / len(sentences), 4),
            'negative_ratio': round(negative_count / len(sentences), 4),
            'neutral_ratio': round(neutral_count / len(sentences), 4)
        }

    def analyze_emotional_tone(self, text):
        """
        Comprehensive emotional tone analysis.

        Args:
            text: Full text to analyze

        Returns:
            Dictionary of emotional metrics
        """
        # Overall sentiment
        vader_scores = self.analyze_with_vader(text)
        textblob_scores = self.analyze_with_textblob(text)

        # Skip detailed sentence-level analysis for performance
        # (analyzing thousands of sentences per text is very slow)
        sentence_dist = {
            'note': 'Sentence-level distribution skipped for performance'
        }

        return {
            'vader': vader_scores,
            'textblob': textblob_scores,
            'sentence_distribution': sentence_dist,
            'overall_tone': self._classify_tone(
                vader_scores['compound'],
                textblob_scores['subjectivity']
            )
        }

    def _classify_tone(self, compound_score, subjectivity):
        """
        Classify overall emotional tone.

        Args:
            compound_score: VADER compound score
            subjectivity: TextBlob subjectivity score

        Returns:
            Tone classification string
        """
        # Determine sentiment
        if compound_score >= 0.05:
            sentiment = "positive"
        elif compound_score <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Determine objectivity
        if subjectivity < 0.3:
            objectivity = "objective"
        elif subjectivity < 0.6:
            objectivity = "balanced"
        else:
            objectivity = "subjective"

        return f"{sentiment}, {objectivity}"

    def compare_authors_sentiment(self, plato_sentiments, aristotle_sentiments):
        """
        Compare sentiment patterns between Plato and Aristotle.

        Args:
            plato_sentiments: Sentiment data for Plato's texts
            aristotle_sentiments: Sentiment data for Aristotle's texts

        Returns:
            Comparative analysis
        """
        # Average across all texts per author
        plato_polarities = []
        plato_subjectivities = []
        aristotle_polarities = []
        aristotle_subjectivities = []

        for sentiment in plato_sentiments.values():
            plato_polarities.append(sentiment['textblob']['polarity'])
            plato_subjectivities.append(sentiment['textblob']['subjectivity'])

        for sentiment in aristotle_sentiments.values():
            aristotle_polarities.append(sentiment['textblob']['polarity'])
            aristotle_subjectivities.append(sentiment['textblob']['subjectivity'])

        return {
            'plato': {
                'avg_polarity': round(np.mean(plato_polarities), 4),
                'avg_subjectivity': round(np.mean(plato_subjectivities), 4)
            },
            'aristotle': {
                'avg_polarity': round(np.mean(aristotle_polarities), 4),
                'avg_subjectivity': round(np.mean(aristotle_subjectivities), 4)
            },
            'comparison': {
                'polarity_difference': round(np.mean(plato_polarities) - np.mean(aristotle_polarities), 4),
                'subjectivity_difference': round(np.mean(plato_subjectivities) - np.mean(aristotle_subjectivities), 4),
                'interpretation': self._interpret_comparison(
                    np.mean(plato_polarities),
                    np.mean(aristotle_polarities),
                    np.mean(plato_subjectivities),
                    np.mean(aristotle_subjectivities)
                )
            }
        }

    def _interpret_comparison(self, plato_pol, aristotle_pol, plato_subj, aristotle_subj):
        """Generate interpretation of sentiment comparison"""
        interpretations = []

        # Polarity comparison
        if abs(plato_pol - aristotle_pol) > 0.05:
            more_positive = "Plato" if plato_pol > aristotle_pol else "Aristotle"
            interpretations.append(f"{more_positive} uses more positive language")
        else:
            interpretations.append("Both authors have similar emotional valence")

        # Subjectivity comparison
        if abs(plato_subj - aristotle_subj) > 0.05:
            more_subjective = "Plato" if plato_subj > aristotle_subj else "Aristotle"
            interpretations.append(f"{more_subjective} writes more subjectively")
        else:
            interpretations.append("Both authors have similar subjectivity levels")

        return " | ".join(interpretations)


def analyze_all_sentiments():
    """
    Run sentiment analysis on all texts.
    """
    processed_dir = Path('data/processed')
    output_dir = Path('output')

    # Load all texts
    txt_files = list(processed_dir.glob('*.txt'))
    if not txt_files:
        print("No texts found. Run extract.py first.")
        return

    analyzer = SentimentAnalyzer()

    print("Analyzing sentiment in all texts...")
    all_sentiments = {}
    plato_sentiments = {}
    aristotle_sentiments = {}

    for txt_path in tqdm(txt_files):
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        text_id = txt_path.stem
        sentiment = analyzer.analyze_emotional_tone(text)
        all_sentiments[text_id] = sentiment

        # Categorize by author
        if 'Plato' in text_id:
            plato_sentiments[text_id] = sentiment
        elif 'Aristotle' in text_id or 'Artistotle' in text_id:
            aristotle_sentiments[text_id] = sentiment

    # Compare authors
    print("\nComparing author sentiment patterns...")
    author_comparison = analyzer.compare_authors_sentiment(plato_sentiments, aristotle_sentiments)

    # Compile results
    results = {
        'individual_texts': all_sentiments,
        'author_comparison': author_comparison
    }

    # Save results
    output_path = output_dir / 'sentiment.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\nSentiment analysis complete! Results saved to {output_path}")

    # Print summary
    print("\n" + "="*60)
    print("SENTIMENT SUMMARY")
    print("="*60)
    for text_id, sentiment in all_sentiments.items():
        print(f"\n{text_id}:")
        print(f"  Overall tone: {sentiment['overall_tone']}")
        print(f"  Polarity: {sentiment['textblob']['polarity']:.3f}")
        print(f"  Subjectivity: {sentiment['textblob']['subjectivity']:.3f}")

    print("\n" + "="*60)
    print("PLATO VS ARISTOTLE - SENTIMENT")
    print("="*60)
    print(f"Plato avg polarity: {author_comparison['plato']['avg_polarity']:.3f}")
    print(f"Aristotle avg polarity: {author_comparison['aristotle']['avg_polarity']:.3f}")
    print(f"\nPlato avg subjectivity: {author_comparison['plato']['avg_subjectivity']:.3f}")
    print(f"Aristotle avg subjectivity: {author_comparison['aristotle']['avg_subjectivity']:.3f}")
    print(f"\n{author_comparison['comparison']['interpretation']}")


if __name__ == '__main__':
    analyze_all_sentiments()
