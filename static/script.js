let itsChart = null;
let riskChart = null; // 1. Define global variable

function showView(viewId, event) {
    document.querySelectorAll('.view-section').forEach(v => {
        v.classList.remove('active');
        v.style.display = 'none';
    });

    const target = document.getElementById(viewId);
    if (target) {
        target.classList.add('active');
        target.style.display = 'block';
    }

    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    if (event && event.currentTarget) event.currentTarget.classList.add('active');

    if (viewId === 'risk') {
        setTimeout(() => {
            if (itsChart) itsChart.resize();
            if (riskChart) riskChart.resize();
        }, 100);
    }
}
function updateCharts() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            // Update Line Chart
            if (itsChart && data.trend_labels) {
                itsChart.data.labels = data.trend_labels;
                itsChart.data.datasets[0].data = data.trend_scores;
                itsChart.update();
            }
            // Limit data points (VERY IMPORTANT)
            if (itsChart && itsChart.data.labels.length > 10) {
                itsChart.data.labels.shift();
                itsChart.data.datasets[0].data.shift();
            }
            
                   

            // 2. Update Pie Chart with real data from API
            if (riskChart && data.risk_distribution) {
                riskChart.data.datasets[0].data = data.risk_distribution;
                riskChart.update();
            }
        })
        .catch(err => console.error("Error fetching stats:", err));
}

function runManualAnalysis() {
    const data = {
        hour: document.getElementById('m_hour').value,
        files: document.getElementById('m_files').value,
        transfer: document.getElementById('m_transfer').value,
        device: document.getElementById('m_device').value
    };

    fetch('/api/analyze_manual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(res => {
        const box = document.getElementById('result-box');
        box.style.display = 'block';
        box.style.background = res.severity === 'CRITICAL' ? 'rgba(255,77,77,0.2)' : 'rgba(0,242,255,0.1)';
        box.style.border = res.severity === 'CRITICAL' ? '1px solid #ff4d4d' : '1px solid #00f2ff';
        
        document.getElementById('result-text').innerText = `ML Prediction: ${res.severity}`;
        document.getElementById('result-text').style.color = res.severity === 'CRITICAL' ? '#ff4d4d' : '#00f2ff';
        document.getElementById('result-score').innerText = `ITS Score: ${res.score}/100`;
    });
}

// 3. Initialize both charts once when the page loads
document.addEventListener("DOMContentLoaded", () => {
    // Initialize Line Chart
    const lineCtx = document.getElementById('itsChart');
    if (lineCtx) {
        itsChart = new Chart(lineCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{ 
                    label: 'Risk Trend', 
                    data: [], 
                    borderColor: '#00f2ff', 
                    backgroundColor: 'rgba(0, 242, 255, 0.1)',
                    fill: true,
                    tension: 0.4 
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    // 4. Initialize Pie Chart ONCE
    const pieCtx = document.getElementById('riskPieChart');
    if (pieCtx) {
        riskChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: ['Normal', 'Medium', 'Critical'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [
                    '#22c55e',   // Green - Normal
                    '#f59e0b',   // Orange - Medium
                    '#ff4d4d'    // Red - Critical
                ],
                    borderWidth: 0
                }]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        labels: { 
                            color: '#e2e8f0',
                            font: { size: 12 }
                        } 
                    }
                }
            }
        });
    }

    // Initial fetch and start interval
    updateCharts();
    setInterval(updateCharts, 5000);
});