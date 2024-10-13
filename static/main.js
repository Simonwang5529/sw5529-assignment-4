document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('search-form');
    const resultsDiv = document.getElementById('results');
    const canvas = document.getElementById('similarity-chart');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const query = document.getElementById('query').value;

        fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ 'query': query })
        })
        .then(response => response.json())
        .then(data => {
            // Display the top 5 results
            let resultsHTML = '<h2>Top 5 Results:</h2>';
            data.documents.forEach((doc, index) => {
                resultsHTML += `<p><strong>Document ${index+1}:</strong> (Similarity: ${data.similarities[index].toFixed(2)}) ${doc.substring(0, 200)}...</p>`;
            });
            resultsDiv.innerHTML = resultsHTML;

            // Destroy previous chart if it exists
            if (window.myChart) {
                window.myChart.destroy();
            }

            // Render the similarity chart using Chart.js
            const ctx = canvas.getContext('2d');
            window.myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Doc 1', 'Doc 2', 'Doc 3', 'Doc 4', 'Doc 5'],
                    datasets: [{
                        label: 'Cosine Similarity',
                        data: data.similarities,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});