# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a distant reading analysis project focused on classical philosophical texts. "Distant reading" is a computational approach to literary and textual analysis, involving quantitative analysis of large text corpora.

## Current State

The repository currently contains source documents only:
- **Aristotle**: Government/Politics, Poetics, Ethics
- **Plato**: Phaedo, Republic, Symposium

All texts are in Microsoft Word (.docx) format and will need to be extracted/processed for analysis.

## Source Documents

Located in the root directory:
- `Aristotle Gov.docx` - Aristotle's Politics/Government
- `Aristotle Poetics.docx` - Aristotle's Poetics
- `Artistotle Ethics.docx` - Aristotle's Nicomachean Ethics (note: filename has typo)
- `Plato Phae.docx` - Plato's Phaedo
- `Plato Republic.docx` - Plato's Republic
- `Plato Symp.docx` - Plato's Symposium

## Expected Development

When implementing code for this project, consider:

1. **Text Extraction**: Need to extract text from .docx files (python-docx library recommended)
2. **Text Processing**: Likely will use NLP libraries (NLTK, spaCy, or similar)
3. **Analysis Pipeline**: Structure for preprocessing, analyzing, and visualizing textual data
4. **Output**: May include statistical analysis, word frequency, topic modeling, sentiment analysis, or comparative analysis across texts

## Project Structure (To Be Implemented)

Typical structure for a distant reading project might include:
- `/data/raw/` - Original source documents
- `/data/processed/` - Extracted and cleaned text files
- `/src/` or `/scripts/` - Analysis code
- `/notebooks/` - Jupyter notebooks for exploratory analysis
- `/output/` or `/results/` - Generated visualizations and analysis results
- `requirements.txt` or `environment.yml` - Python dependencies
