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

## Quick Start (No Installation Required!)

**All analysis data is pre-generated and included in this repository.** You can use the interactive dashboard immediately without installing anything:

### Option 1: Local Viewing
Simply open `web/index.html` in your web browser.

### Option 2: GitHub Pages Deployment
1. Push this repository to GitHub
2. Go to Settings → Pages
3. Set Source to your main branch
4. Set folder to `/` (root)
5. Your site will be live at `https://[username].github.io/[repo-name]/web/`

### Option 3: Other Static Hosting
Deploy the entire repository to any static hosting service (Netlify, Vercel, etc.) and access `web/index.html`.

## Re-running Analysis (Optional)

If you want to modify the texts or re-run the analysis:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"

# Run analysis pipeline
python src/extract.py      # Extract from .docx
python src/preprocess.py   # Clean text
python src/analyze.py      # Analyze vocabulary
python src/topics.py       # Topic modeling
python src/generate.py     # Generate final JSON
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
