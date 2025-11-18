// Word Cloud Visualization
let wordcloudData = null;

function initWordcloud(data) {
    wordcloudData = data;

    // Set up wordcloud selector
    const selector = document.getElementById('wordcloud-select');
    selector.addEventListener('change', (e) => {
        renderWordcloud(e.target.value);
    });

    // Render initial wordcloud (all texts)
    renderWordcloud('all');
}

function renderWordcloud(selection) {
    const container = document.getElementById('wordcloud');
    container.innerHTML = ''; // Clear previous wordcloud

    let wordList = [];

    if (selection === 'all') {
        // Combine all texts
        const allWords = {};
        Object.values(wordcloudData.text_stats).forEach(textStats => {
            textStats.top_words.forEach(([word, count]) => {
                allWords[word] = (allWords[word] || 0) + count;
            });
        });

        wordList = Object.entries(allWords)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 100)
            .map(([word, count]) => [word, count]);

    } else if (selection === 'plato') {
        // Plato's texts only
        const platoWords = {};
        wordcloudData.metadata.texts.plato.forEach(textId => {
            wordcloudData.text_stats[textId].top_words.forEach(([word, count]) => {
                platoWords[word] = (platoWords[word] || 0) + count;
            });
        });

        wordList = Object.entries(platoWords)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 100)
            .map(([word, count]) => [word, count]);

    } else if (selection === 'aristotle') {
        // Aristotle's texts only
        const aristotleWords = {};
        wordcloudData.metadata.texts.aristotle.forEach(textId => {
            wordcloudData.text_stats[textId].top_words.forEach(([word, count]) => {
                aristotleWords[word] = (aristotleWords[word] || 0) + count;
            });
        });

        wordList = Object.entries(aristotleWords)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 100)
            .map(([word, count]) => [word, count]);
    }

    // Check if wordcloud2 is available
    if (typeof WordCloud === 'undefined') {
        container.innerHTML = '<p>WordCloud library not loaded. Please check your internet connection.</p>';
        return;
    }

    // Prepare data for wordcloud2
    const maxCount = Math.max(...wordList.map(([_, count]) => count));
    const cloudData = wordList.map(([word, count]) => {
        // Scale size based on frequency (larger words for more frequent terms)
        const size = Math.max(12, Math.min(80, (count / maxCount) * 80));
        return [word, size];
    });

    // Generate color based on selection
    const getColor = () => {
        if (selection === 'plato') {
            const blues = ['#3498db', '#2980b9', '#5dade2', '#85c1e9'];
            return blues[Math.floor(Math.random() * blues.length)];
        } else if (selection === 'aristotle') {
            const reds = ['#e74c3c', '#c0392b', '#ec7063', '#f1948a'];
            return reds[Math.floor(Math.random() * reds.length)];
        } else {
            const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'];
            return colors[Math.floor(Math.random() * colors.length)];
        }
    };

    // Render wordcloud
    try {
        WordCloud(container, {
            list: cloudData,
            gridSize: 8,
            weightFactor: 1,
            fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
            color: getColor,
            rotateRatio: 0.3,
            rotationSteps: 2,
            backgroundColor: '#ffffff',
            drawOutOfBound: false,
            shrinkToFit: true
        });
    } catch (error) {
        console.error('Error creating wordcloud:', error);
        container.innerHTML = '<p>Error creating wordcloud. Please refresh the page.</p>';
    }
}
