document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('attackChart').getContext('2d');

    fetch('/dashboard/stats')
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data);
            const values = Object.values(data);

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            '#ff5f5f',
                            '#f5a623',
                            '#50e3c2',
                            '#4a90e2'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#ececec'
                            }
                        }
                    }
                }
            });
        });
});
