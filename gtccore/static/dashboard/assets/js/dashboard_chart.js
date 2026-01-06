// dashboard_chart.js
// Handles rendering of the Applications Analysis chart on the dashboard page

document.addEventListener('DOMContentLoaded', function () {
    const chartEl = document.getElementById('dashboard_applications_chart');
    const errorEl = document.getElementById('dashboard_chart_error');
    let applicationsAnalysis = null;
    try {
        applicationsAnalysis = JSON.parse(document.getElementById('dashboard_applications_data').textContent);
        console.log('Parsed chart data:', applicationsAnalysis);
    } catch (e) {
        console.error('Error parsing chart data:', e);
        if (errorEl) errorEl.style.display = 'block';
        return;
    }
    if (chartEl && applicationsAnalysis) {
        if (!applicationsAnalysis.labels || !applicationsAnalysis.applications || !applicationsAnalysis.admissions) {
            if (errorEl) errorEl.style.display = 'block';
            return;
        }
        const ctx = chartEl.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: applicationsAnalysis.labels,
                datasets: [
                    {
                        label: 'Applications',
                        data: applicationsAnalysis.applications,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        fill: true,
                        tension: 0.4,
                    },
                    {
                        label: 'Admissions',
                        data: applicationsAnalysis.admissions,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        fill: true,
                        tension: 0.4,
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Applications & Admissions (Last 12 Months)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
