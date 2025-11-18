# Distant Reading: Classical Philosophy

A computational textual analysis project examining the connections and influences between Plato and Aristotle through their major works.

## Texts Analyzed

**Plato (Teacher):**
- Phaedo
- Republic
- Symposium

**Aristotle (Student):**
- Politics/Government
- Poetics
- Nicomachean Ethics

## Features

- **Vocabulary Analysis**: Shared terms, unique vocabulary, and lexical diversity
- **Topic Modeling**: Identifying shared philosophical themes across texts
- **Stylistic Comparison**: Sentence complexity, argumentation patterns, vocabulary sophistication
- **Sentiment Analysis**: Emotional tone and rhetorical patterns
- **Influence Detection**: Tracking conceptual connections between teacher and student
- **Interactive Visualizations**: Network graphs, wordclouds, comparative metrics

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
```

## Usage

```bash
# 1. Extract text from Word documents
python src/extract.py

# 2. Preprocess and clean texts
python src/preprocess.py

# 3. Run complete analysis
python src/analyze.py

# 4. Generate web visualization data
python src/generate.py

# 5. Open web interface
# Simply open web/index.html in a browser
```

## Project Structure

```
data/
  raw/          # Original .docx files
  processed/    # Extracted and cleaned text files
src/            # Python analysis scripts
output/         # Generated analysis data (JSON)
web/            # Interactive web dashboard
  index.html    # Main overview of all 6 texts
  compare.html  # Side-by-side comparison tool
  js/           # Visualization JavaScript
  css/          # Styles
```

## Analysis Methods

The project employs computational literary analysis techniques to explore:

1. **Lexical Connections**: Which terms did Aristotle adopt from Plato? Where did he diverge?
2. **Thematic Overlap**: What philosophical themes span both authors' works?
3. **Stylistic Evolution**: How do their writing styles compare?
4. **Conceptual Networks**: How do key concepts interconnect within and across texts?

This "distant reading" approach reveals patterns that emerge across the entire corpus, complementing traditional close reading methods.
