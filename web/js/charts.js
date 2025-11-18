// Charts using Chart.js
function createCharts(data) {
    createSentimentCharts(data);
    createSentenceLengthChart(data);
    createDiversityChart(data);
}

// Sentiment charts
function createSentimentCharts(data) {
    const textIds = Object.keys(data.text_stats);
    const labels = textIds.map(id => id.replace('Plato ', 'P:').replace('Aristotle ', 'A:').replace('Artistotle ', 'A:'));

    // Get sentiment data
    const polarities = textIds.map(id => data.sentiment.individual_texts[id].textblob.polarity);
    const subjectivities = textIds.map(id => data.sentiment.individual_texts[id].textblob.subjectivity);

    // Background colors based on author
    const backgroundColors = textIds.map(id =>
        id.includes('Plato') ? 'rgba(52, 152, 219, 0.7)' : 'rgba(231, 76, 60, 0.7)'
    );
    const borderColors = textIds.map(id =>
        id.includes('Plato') ? 'rgba(52, 152, 219, 1)' : 'rgba(231, 76, 60, 1)'
    );

    // Polarity chart
    const polarityCtx = document.getElementById('sentiment-polarity-chart');
    if (polarityCtx) {
        new Chart(polarityCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Polarity (-1 = Negative, +1 = Positive)',
                    data: polarities,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        min: -1,
                        max: 1
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Subjectivity chart
    const subjectivityCtx = document.getElementById('sentiment-subjectivity-chart');
    if (subjectivityCtx) {
        new Chart(subjectivityCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Subjectivity (0 = Objective, 1 = Subjective)',
                    data: subjectivities,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        min: 0,
                        max: 1
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Sentence length chart
function createSentenceLengthChart(data) {
    const textIds = Object.keys(data.text_stats);
    const labels = textIds.map(id => id.replace('Plato ', 'P:').replace('Aristotle ', 'A:').replace('Artistotle ', 'A:'));

    const avgSentenceLengths = textIds.map(id =>
        data.text_stats[id].sentence_stats.avg_sentence_length
    );

    const backgroundColors = textIds.map(id =>
        id.includes('Plato') ? 'rgba(52, 152, 219, 0.7)' : 'rgba(231, 76, 60, 0.7)'
    );
    const borderColors = textIds.map(id =>
        id.includes('Plato') ? 'rgba(52, 152, 219, 1)' : 'rgba(231, 76, 60, 1)'
    );

    const ctx = document.getElementById('sentence-length-chart');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Average Words per Sentence',
                    data: avgSentenceLengths,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Lexical diversity chart
function createDiversityChart(data) {
    const textIds = Object.keys(data.text_stats);
    const labels = textIds.map(id => id.replace('Plato ', 'P:').replace('Aristotle ', 'A:').replace('Artistotle ', 'A:'));

    const ttrValues = textIds.map(id =>
        data.text_stats[id].lexical_diversity.ttr
    );

    const mtldValues = textIds.map(id =>
        data.text_stats[id].lexical_diversity.mtld
    );

    const backgroundColors = textIds.map(id =>
        id.includes('Plato') ? 'rgba(52, 152, 219, 0.7)' : 'rgba(231, 76, 60, 0.7)'
    );
    const borderColors = textIds.map(id =>
        id.includes('Plato') ? 'rgba(52, 152, 219, 1)' : 'rgba(231, 76, 60, 1)'
    );

    const ctx = document.getElementById('diversity-chart');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'TTR (Type-Token Ratio)',
                        data: ttrValues,
                        backgroundColor: backgroundColors,
                        borderColor: borderColors,
                        borderWidth: 2,
                        yAxisID: 'y'
                    },
                    {
                        label: 'MTLD (Measure of Textual Lexical Diversity)',
                        data: mtldValues,
                        backgroundColor: backgroundColors.map(c => c.replace('0.7', '0.4')),
                        borderColor: borderColors,
                        borderWidth: 2,
                        borderDash: [5, 5],
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'TTR'
                        },
                        beginAtZero: true
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'MTLD'
                        },
                        beginAtZero: true,
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
}
