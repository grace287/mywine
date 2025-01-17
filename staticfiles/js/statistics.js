// 차트 기본 설정
Chart.defaults.font.family = "'Noto Sans KR', sans-serif";
Chart.defaults.color = '#2d3436';

// 맛 프로필 레이더 차트
function initTasteProfileChart(data) {
    new Chart(document.getElementById('tasteProfileChart'), {
        type: 'radar',
        data: {
            labels: ['당도', '산도', '탄닌', '바디'],
            datasets: [{
                label: '평균 맛 프로필',
                data: [
                    data.sweetness,
                    data.acidity,
                    data.tannin,
                    data.body
                ],
                backgroundColor: 'rgba(108, 92, 231, 0.2)',
                borderColor: '#6c5ce7',
                pointBackgroundColor: '#6c5ce7',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#6c5ce7'
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        stepSize: 1
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    angleLines: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    pointLabels: {
                        font: {
                            size: 14
                        }
                    }
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

// 와인 타입 도넛 차트
function initWineTypeChart(data) {
    new Chart(document.getElementById('wineTypeChart'), {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.type),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: [
                    '#e74c3c',
                    '#f1c40f',
                    '#3498db',
                    '#e84393'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// 지역별 막대 차트
function initRegionChart(data) {
    new Chart(document.getElementById('regionChart'), {
        type: 'bar',
        data: {
            labels: data.map(item => item.country),
            datasets: [{
                label: '와인 수',
                data: data.map(item => item.count),
                backgroundColor: '#6c5ce7'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
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

// 차트 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 예시 데이터 (서버에서 가져온 데이터로 대체)
    const statisticsData = {
        totalWines: 5,
        averageRating: 4.0,
        averagePrice: 15000,
        preferredWineType: "레드",
        preferredAroma: "과일 향"
    };

    // DOM 요소에 데이터 삽입
    document.getElementById('total-wines').textContent = statisticsData.totalWines + '개';
    document.getElementById('average-rating').textContent = statisticsData.averageRating + ' ★';
    document.getElementById('average-price').textContent = statisticsData.averagePrice + ' 원';
    document.getElementById('preferred-wine-type').textContent = statisticsData.preferredWineType;
    document.getElementById('preferred-aroma').textContent = statisticsData.preferredAroma;
}); 