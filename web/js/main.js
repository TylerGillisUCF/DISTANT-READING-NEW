// Main Dashboard JavaScript
let analysisData = null;

// Load analysis data
async function loadData() {
    try {
        const response = await fetch('../output/full_analysis.json');
        if (!response.ok) {
            throw new Error('Analysis data not found. Please run the analysis pipeline first.');
        }
        analysisData = await response.json();
        initializeDashboard();
    } catch (error) {
        document.getElementById('loading').innerHTML = `
            <h2>Error Loading Data</h2>
            <p>${error.message}</p>
            <p>Please run the following commands:</p>
            <pre>
python src/extract.py
python src/preprocess.py
python src/analyze.py
python src/topics.py
python src/sentiment.py
python src/generate.py
            </pre>
        `;
    }
}

// Initialize dashboard with loaded data
function initializeDashboard() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';

    displaySummaryStats();
    displayTextCards();
    displayAuthorComparison();
    displaySharedThemes();
    displaySentimentAnalysis();

    // Initialize visualizations
    if (typeof createNetwork === 'function') {
        createNetwork(analysisData.network);
    }
    if (typeof initWordcloud === 'function') {
        initWordcloud(analysisData);
    }
    if (typeof createCharts === 'function') {
        createCharts(analysisData);
    }
}

// Display summary statistics
function displaySummaryStats() {
    const totalWords = Object.values(analysisData.text_stats)
        .reduce((sum, text) => sum + text.basic_stats.word_count, 0);

    document.getElementById('total-texts').textContent = analysisData.metadata.text_count;
    document.getElementById('total-words').textContent = totalWords.toLocaleString();
    document.getElementById('shared-vocab').textContent =
        analysisData.vocabulary_analysis.shared_vocabulary.toLocaleString();
}

// Display individual text cards
function displayTextCards() {
    const container = document.getElementById('text-cards');
    container.innerHTML = '';

    Object.entries(analysisData.text_stats).forEach(([textId, stats]) => {
        const authorClass = textId.includes('Plato') ? 'plato' : 'aristotle';
        const author = textId.includes('Plato') ? 'Plato' : 'Aristotle';

        const card = document.createElement('div');
        card.className = `text-card ${authorClass}`;
        card.innerHTML = `
            <h3>${textId}</h3>
            <div class="author">${author}</div>
            <div class="stat">
                <span class="stat-label">Words</span>
                <span class="stat-value">${stats.basic_stats.word_count.toLocaleString()}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Unique Words</span>
                <span class="stat-value">${stats.basic_stats.vocabulary_size.toLocaleString()}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Sentences</span>
                <span class="stat-value">${stats.basic_stats.sentence_count.toLocaleString()}</span>
            </div>
            <div class="stat">
                <span class="stat-label">Lexical Diversity</span>
                <span class="stat-value">${stats.lexical_diversity.ttr.toFixed(3)}</span>
            </div>
        `;

        container.appendChild(card);
    });
}

// Display author comparison
function displayAuthorComparison() {
    const vocab = analysisData.vocabulary_analysis;

    document.getElementById('plato-vocab').textContent = vocab.plato_vocabulary_size.toLocaleString();
    document.getElementById('aristotle-vocab').textContent = vocab.aristotle_vocabulary_size.toLocaleString();

    // Calculate average lexical diversity
    const platoTexts = analysisData.metadata.texts.plato;
    const aristotleTexts = analysisData.metadata.texts.aristotle;

    const platoDiversity = platoTexts.reduce((sum, id) =>
        sum + analysisData.text_stats[id].lexical_diversity.ttr, 0) / platoTexts.length;

    const aristotleDiversity = aristotleTexts.reduce((sum, id) =>
        sum + analysisData.text_stats[id].lexical_diversity.ttr, 0) / aristotleTexts.length;

    document.getElementById('plato-diversity').textContent = platoDiversity.toFixed(3);
    document.getElementById('aristotle-diversity').textContent = aristotleDiversity.toFixed(3);

    // Display shared words
    const sharedWordsContainer = document.getElementById('shared-words');
    sharedWordsContainer.innerHTML = '';

    vocab.top_shared_words.slice(0, 30).forEach(item => {
        const wordItem = document.createElement('div');
        wordItem.className = 'word-item';
        wordItem.innerHTML = `
            <span class="word">${item.word}</span>
            <span class="count">P:${item.plato_count} A:${item.aristotle_count}</span>
        `;
        sharedWordsContainer.appendChild(wordItem);
    });
}

// Display shared themes/topics
function displaySharedThemes() {
    const container = document.getElementById('topics-container');
    container.innerHTML = '';

    const topics = analysisData.topics.topic_keywords;
    const sharedThemes = analysisData.topics.shared_themes.shared_themes;

    sharedThemes.slice(0, 6).forEach(theme => {
        const topicData = topics[theme.topic];
        const themeDiv = document.createElement('div');
        themeDiv.className = 'card';
        themeDiv.style.backgroundColor = '#f8f9fa';
        themeDiv.style.marginBottom = '1rem';
        themeDiv.innerHTML = `
            <h3>${theme.topic.toUpperCase()}</h3>
            <div class="metric-row">
                <span class="metric-label">Plato Strength</span>
                <span class="metric-value">${(theme.plato_strength * 100).toFixed(1)}%</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Aristotle Strength</span>
                <span class="metric-value">${(theme.aristotle_strength * 100).toFixed(1)}%</span>
            </div>
            <div class="topic-tag-container" style="margin-top: 1rem;">
                <strong>Keywords:</strong>
                ${topicData.keywords.slice(0, 10).map(word =>
                    `<span class="topic-tag">${word}</span>`
                ).join('')}
            </div>
        `;
        container.appendChild(themeDiv);
    });
}

// Display sentiment analysis
function displaySentimentAnalysis() {
    const sentimentData = analysisData.sentiment;
    const comparison = sentimentData.author_comparison;

    const comparisonDiv = document.getElementById('author-sentiment-comparison');
    comparisonDiv.innerHTML = `
        <div class="grid grid-2">
            <div>
                <h4 class="plato-text">Plato</h4>
                <div class="metric-row">
                    <span class="metric-label">Avg Polarity</span>
                    <span class="metric-value">${comparison.plato.avg_polarity.toFixed(3)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Avg Subjectivity</span>
                    <span class="metric-value">${comparison.plato.avg_subjectivity.toFixed(3)}</span>
                </div>
            </div>
            <div>
                <h4 class="aristotle-text">Aristotle</h4>
                <div class="metric-row">
                    <span class="metric-label">Avg Polarity</span>
                    <span class="metric-value">${comparison.aristotle.avg_polarity.toFixed(3)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Avg Subjectivity</span>
                    <span class="metric-value">${comparison.aristotle.avg_subjectivity.toFixed(3)}</span>
                </div>
            </div>
        </div>
        <div class="mt-2" style="padding: 1rem; background-color: #f8f9fa; border-radius: 4px;">
            <strong>Interpretation:</strong> ${comparison.comparison.interpretation}
        </div>
    `;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadData);
