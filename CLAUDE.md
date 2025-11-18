# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a distant reading analysis project focused on classical philosophical texts. "Distant reading" is a computational approach to literary and textual analysis, involving quantitative analysis of large text corpora.

## Project Goal

Analyze connections and influences between Plato (teacher) and Aristotle (student) through computational textual analysis. The system examines all 6 classical texts for:
- Shared vocabulary and conceptual connections
- Lexical diversity and stylistic patterns
- Topic modeling and thematic overlap
- Sentiment and rhetorical patterns
- Teacher-student influence detection

## Source Documents

Located in `data/raw/`:
- **Aristotle**: `Aristotle Gov.docx`, `Aristotle Poetics.docx`, `Artistotle Ethics.docx` (note typo in filename)
- **Plato**: `Plato Phae.docx`, `Plato Republic.docx`, `Plato Symp.docx`

## Setup and Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (required for text processing)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
```

## Common Commands

```bash
# Full analysis pipeline (run in order)
python src/extract.py      # Extract text from .docx files
python src/preprocess.py   # Clean and normalize text
python src/analyze.py      # Run all analyses
python src/generate.py     # Create JSON for web visualization

# View results
# Open web/index.html in browser for interactive dashboard
```

## Architecture

**Analysis Pipeline (Python):**
- `src/extract.py` - Extracts text from Word documents using python-docx
- `src/preprocess.py` - Cleans text, tokenizes, removes stopwords, normalizes
- `src/analyze.py` - Core analysis engine:
  - Word frequency and vocabulary statistics
  - Lexical diversity (TTR, MTLD)
  - Stylistic metrics (sentence length, complexity)
  - Shared vocabulary detection
- `src/topics.py` - Topic modeling using LDA (Gensim)
- `src/sentiment.py` - Sentiment analysis using VADER and TextBlob
- `src/generate.py` - Exports all analysis data to JSON for web interface

**Visualization (HTML/JavaScript):**
- `web/index.html` - Main dashboard showing all 6 texts
- `web/compare.html` - Side-by-side comparison of any 2 texts
- Uses D3.js for network graphs, wordcloud2.js for interactive wordclouds, Chart.js for metrics

**Data Flow:**
1. Word documents → `extract.py` → plain text files in `data/processed/`
2. Plain text → `preprocess.py` → cleaned/tokenized text
3. Processed text → `analyze.py` + `topics.py` + `sentiment.py` → analysis results
4. Results → `generate.py` → `output/analysis.json`
5. JSON data → loaded by web interface → interactive visualizations

## Project Structure

```
data/
  raw/          # Original .docx files
  processed/    # Extracted .txt files
src/            # Python analysis scripts
output/         # Generated JSON data
web/            # Interactive web dashboard
  js/           # Visualization code
  css/          # Styles
```

## Key Analysis Features

**Vocabulary Overlap**: Detects shared terms between Plato and Aristotle to identify influence
**Topic Modeling**: Uses LDA to find shared philosophical themes across all texts
**Stylistic Fingerprints**: Compares sentence patterns, vocabulary richness, argument structure
**Conceptual Networks**: Maps how key terms co-occur and connect across texts
