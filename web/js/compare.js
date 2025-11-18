// Comparison Page JavaScript
let analysisData = null;
let currentComparison = null;

// Load analysis data
async function loadData() {
    try {
        const response = await fetch('../output/full_analysis.json');
        if (!response.ok) {
            throw new Error('Analysis data not found');
        }
        analysisData = await response.json();
        populateSelectors();
    } catch (error) {
        alert('Error loading data: ' + error.message);
    }
}

// Populate text selectors
function populateSelectors() {
    const select1 = document.getElementById('text1-select');
    const select2 = document.getElementById('text2-select');

    const textIds = Object.keys(analysisData.text_stats);

    textIds.forEach(textId => {
        const option1 = document.createElement('option');
        option1.value = textId;
        option1.textContent = textId;
        select1.appendChild(option1);

        const option2 = document.createElement('option');
        option2.value = textId;
        option2.textContent = textId;
        select2.appendChild(option2);
    });

    // Add compare button listener
    document.getElementById('compare-btn').addEventListener('click', compareTexts);
}

// Compare selected texts
function compareTexts() {
    const text1Id = document.getElementById('text1-select').value;
    const text2Id = document.getElementById('text2-select').value;

    if (!text1Id || !text2Id) {
        alert('Please select both texts to compare');
        return;
    }

    if (text1Id === text2Id) {
        alert('Please select two different texts');
        return;
    }

    // Get data for both texts
    const text1Data = analysisData.text_stats[text1Id];
    const text2Data = analysisData.text_stats[text2Id];

    // Find pairwise comparison
    const pairKey1 = `${text1Id}|||${text2Id}`;
    const pairKey2 = `${text2Id}|||${text1Id}`;
    const overlapData = analysisData.pairwise_comparisons[pairKey1] || analysisData.pairwise_comparisons[pairKey2];

    currentComparison = {
        text1: { id: text1Id, data: text1Data },
        text2: { id: text2Id, data: text2Data },
        overlap: overlapData
    };

    displayComparison();
}

// Display comparison results
function displayComparison() {
    document.getElementById('comparison-results').style.display = 'block';

    const { text1, text2, overlap } = currentComparison;

    // Update titles
    document.getElementById('text1-title').textContent = text1.id;
    document.getElementById('text2-title').textContent = text2.id;

    // Basic stats
    document.getElementById('text1-words').textContent = text1.data.basic_stats.word_count.toLocaleString();
    document.getElementById('text2-words').textContent = text2.data.basic_stats.word_count.toLocaleString();

    document.getElementById('text1-unique').textContent = text1.data.basic_stats.vocabulary_size.toLocaleString();
    document.getElementById('text2-unique').textContent = text2.data.basic_stats.vocabulary_size.toLocaleString();

    document.getElementById('text1-sentences').textContent = text1.data.basic_stats.sentence_count.toLocaleString();
    document.getElementById('text2-sentences').textContent = text2.data.basic_stats.sentence_count.toLocaleString();

    document.getElementById('text1-avg-sent').textContent = text1.data.sentence_stats.avg_sentence_length.toFixed(1);
    document.getElementById('text2-avg-sent').textContent = text2.data.sentence_stats.avg_sentence_length.toFixed(1);

    document.getElementById('text1-ttr').textContent = text1.data.lexical_diversity.ttr.toFixed(3);
    document.getElementById('text2-ttr').textContent = text2.data.lexical_diversity.ttr.toFixed(3);

    // Vocabulary overlap
    document.getElementById('overlap-shared').textContent = overlap.shared_words.toLocaleString();
    document.getElementById('overlap-jaccard').textContent = (overlap.jaccard_similarity * 100).toFixed(1) + '%';

    // Shared words list
    const sharedWordsList = document.getElementById('shared-words-list');
    sharedWordsList.innerHTML = '';
    overlap.shared_words_list.slice(0, 20).forEach(word => {
        const wordItem = document.createElement('div');
        wordItem.className = 'word-item';
        wordItem.innerHTML = `<span class="word">${word}</span>`;
        sharedWordsList.appendChild(wordItem);
    });

    // Top words for each text
    displayTopWords('text1', text1);
    displayTopWords('text2', text2);

    // Sentiment
    displaySentiment('text1', text1.id);
    displaySentiment('text2', text2.id);

    // Create visualizations
    createOverlapChart(overlap, text1.id, text2.id);
    createTopicComparisonChart(text1.id, text2.id);
}

// Display top words for a text
function displayTopWords(prefix, textData) {
    const container = document.getElementById(`${prefix}-top-words`);
    document.getElementById(`${prefix}-top-words-title`).textContent = `${textData.id} - Top Words`;

    container.innerHTML = '';
    textData.data.top_words.slice(0, 20).forEach(([word, count]) => {
        const wordItem = document.createElement('div');
        wordItem.className = 'word-item';
        wordItem.innerHTML = `
            <span class="word">${word}</span>
            <span class="count">${count}</span>
        `;
        container.appendChild(wordItem);
    });
}

// Display sentiment data
function displaySentiment(prefix, textId) {
    const sentimentData = analysisData.sentiment.individual_texts[textId];

    document.getElementById(`${prefix}-sentiment-title`).textContent = `${textId} - Sentiment`;
    document.getElementById(`${prefix}-polarity`).textContent = sentimentData.textblob.polarity.toFixed(3);
    document.getElementById(`${prefix}-subjectivity`).textContent = sentimentData.textblob.subjectivity.toFixed(3);
    document.getElementById(`${prefix}-tone`).textContent = sentimentData.overall_tone;
}

// Create overlap chart
function createOverlapChart(overlap, text1Id, text2Id) {
    const ctx = document.getElementById('overlap-chart');

    if (ctx.chart) {
        ctx.chart.destroy();
    }

    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Shared', `Unique to ${text1Id}`, `Unique to ${text2Id}`],
            datasets: [{
                data: [
                    overlap.shared_words,
                    overlap.unique_to_first,
                    overlap.unique_to_second
                ],
                backgroundColor: [
                    'rgba(46, 204, 113, 0.7)',
                    'rgba(52, 152, 219, 0.7)',
                    'rgba(231, 76, 60, 0.7)'
                ],
                borderColor: [
                    'rgba(46, 204, 113, 1)',
                    'rgba(52, 152, 219, 1)',
                    'rgba(231, 76, 60, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    ctx.chart = chart;
}

// Create topic comparison chart
function createTopicComparisonChart(text1Id, text2Id) {
    const ctx = document.getElementById('topic-comparison-chart');

    if (ctx.chart) {
        ctx.chart.destroy();
    }

    const topics = analysisData.topics.topic_keywords;
    const text1Topics = analysisData.topics.document_topics[text1Id] || {};
    const text2Topics = analysisData.topics.document_topics[text2Id] || {};

    const topicLabels = Object.keys(topics).map(t => t.replace('topic_', 'Topic '));
    const text1Values = Object.keys(topics).map(t => text1Topics[t] || 0);
    const text2Values = Object.keys(topics).map(t => text2Topics[t] || 0);

    const chart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: topicLabels,
            datasets: [
                {
                    label: text1Id,
                    data: text1Values,
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 2
                },
                {
                    label: text2Id,
                    data: text2Values,
                    backgroundColor: 'rgba(231, 76, 60, 0.2)',
                    borderColor: 'rgba(231, 76, 60, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });

    ctx.chart = chart;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadData);
