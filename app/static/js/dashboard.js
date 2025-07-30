let dashboardData = null;

const sidebar = document.getElementById('sidebar');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebarOverlay = document.getElementById('sidebarOverlay');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        sidebarOverlay.classList.toggle('active');
    });
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    });
}

window.addEventListener('resize', () => {
    if (window.innerWidth > 1024) {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    }
});

// Fetch GitHub stars
async function fetchGitHubStars() {
    try {
        const response = await fetch('https://api.github.com/repos/primeZdev/walpanel');
        const data = await response.json();
        const starsElement = document.getElementById('github-stars');
        if (starsElement) {
            starsElement.textContent = data.stargazers_count || 0;
        }
    } catch (error) {
        console.error('Error fetching GitHub stars:', error);
        const starsElement = document.getElementById('github-stars');
        if (starsElement) {
            starsElement.textContent = '0';
        }
    }
}

// Fetch dashboard data from API
async function fetchDashboardData() {
    try {
        const response = await fetch('/dashboard/data', {
            credentials: 'include'
        });

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to fetch dashboard data');
        }

        dashboardData = await response.json();
        updateDashboardStats();
        updateAdminsChart();
        updatePurchaseChart();
        updateLogs();
        updateSponsorAd();
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        showError('Failed to load dashboard data');
    }
}

function updateDashboardStats() {
    if (!dashboardData) return;

    const panelsElement = document.getElementById('panels-count');
    if (panelsElement) {
        panelsElement.textContent = dashboardData.panels || 0;
    }

    const adminsElement = document.getElementById('admins-count');
    if (adminsElement) {
        adminsElement.textContent = dashboardData.admins ? dashboardData.admins.length : 0;
    }

    const usersElement = document.getElementById('users-count');
    if (usersElement) {
        usersElement.textContent = dashboardData.users || 0;
    }

    const plansElement = document.getElementById('plans-count');
    if (plansElement) {
        plansElement.textContent = dashboardData.plans || 0;
    }
}

function updateSponsorAd() {
    if (!dashboardData || !dashboardData.ads) return;
    const ad = dashboardData.ads;
    const adTitle = document.getElementById('ad-title');
    const adText = document.getElementById('ad-text');
    const adLink = document.getElementById('ad-link');
    const adButton = document.getElementById('ad-button');
    if (adTitle) adTitle.textContent = ad.title || '';
    if (adText) adText.textContent = ad.text || '';
    if (adLink) {
        adLink.href = ad.link || '#';
        adLink.textContent = ad.button || '';
    }
}

function updateAdminsChart() {
    if (!dashboardData || !dashboardData.admins || !Array.isArray(dashboardData.admins)) return;

    const ctx = document.getElementById('adminsPieChart');
    if (!ctx) return;

    const adminsData = dashboardData.admins;
    if (adminsData.length === 0) return;

    const adminNames = adminsData.map(admin => admin.username);
    const adminClients = adminsData.map(admin => admin.total_clients || 0);
    const pieColors = [
        '#4e79a7', '#76b7b2', '#59a14f', '#edc949', '#f28e2b', 
        '#e15759', '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab'
    ];

    let selectedIndex = -1;

    const centerTextPlugin = {
        id: 'centerText',
        beforeDraw: function(chart) {
            const ctx = chart.ctx;
            const width = chart.width;
            const height = chart.height;
            
            ctx.save();
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            if (selectedIndex >= 0 && selectedIndex < adminNames.length) {
                const name = adminNames[selectedIndex];
                const clients = adminClients[selectedIndex];
                const color = pieColors[selectedIndex % pieColors.length];

                ctx.fillStyle = color;
                ctx.font = 'bold 16px Arial';
                ctx.fillText(name, width / 2, height / 2 - 10);

                ctx.fillStyle = '#fff';
                ctx.font = '14px Arial';
                ctx.fillText(clients + ' users', width / 2, height / 2 + 10);
            } else {
                ctx.font = '12px Arial';
                const fontSize = 12;
                const startY = height / 2 - (adminNames.length * fontSize) / 2;

                adminNames.forEach((name, i) => {
                    ctx.fillStyle = pieColors[i % pieColors.length];
                    ctx.fillText(name, width / 2, startY + i * fontSize);
                });
            }
            ctx.restore();
        }
    };

    // Create chart
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: adminNames,
            datasets: [{
                data: adminClients,
                backgroundColor: pieColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            cutout: '85%',
            plugins: {
                legend: {
                    display: false
                },
                datalabels: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            return 'total users: ' + value;
                        }
                    }
                }
            },
            onClick: function(evt, elements) {
                if (elements.length > 0) {
                    selectedIndex = elements[0].index;
                    this.update();
                }
            }
        },
        plugins: [centerTextPlugin, ChartDataLabels]
    });
}

function updatePurchaseChart() {
    if (!dashboardData || !dashboardData.purchases) return;

    const ctx = document.getElementById('purchaseChart');
    if (!ctx) return;

    const purchases = dashboardData.purchases;

    updatePurchaseStats(purchases);

    if (!purchases.purchases || purchases.purchases.length === 0) {
        showEmptyPurchaseChart(ctx);
        return;
    }

    const purchaseData = processPurchaseData(purchases.purchases);
    createAdvancedPurchaseChart(ctx, purchaseData);
}

// Update purchase statistics
function updatePurchaseStats(purchases) {
    const successfulPurchasesElement = document.getElementById('successfulPurchases');
    const failedPurchasesElement = document.getElementById('failedPurchases');
    const totalRevenueElement = document.getElementById('totalRevenue');

    if (purchases.purchases && Array.isArray(purchases.purchases)) {
        if (successfulPurchasesElement) {
            const successfulCount = purchases.purchases.filter(purchase =>
                purchase.status === 'done'
            ).length;
            successfulPurchasesElement.textContent = successfulCount;
        }

        if (failedPurchasesElement) {
            const failedCount = purchases.purchases.filter(purchase =>
                purchase.status !== 'done'
            ).length;
            failedPurchasesElement.textContent = failedCount;
        }

        if (totalRevenueElement) {
            const totalRevenue = purchases.purchases.reduce((sum, purchase) => {
                if (purchase.status === 'done') {
                    return sum + (purchase.amount || 0);
                }
                return sum;
            }, 0);
            totalRevenueElement.textContent = `${totalRevenue.toLocaleString()} $/T`;
        }
    }
}

function processPurchaseData(purchases) {
    const last7Days = [];
    const today = new Date();

    // Generate last 7 days
    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        last7Days.push({
            date: date.toISOString().split('T')[0],
            label: date.toLocaleDateString('en-US', { weekday: 'short' }),
            fullDate: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
            successfulCount: 0,
            failedCount: 0,
            successfulAmount: 0,
            failedAmount: 0,
            successfulPurchases: [],
            failedPurchases: []
        });
    }

    purchases.forEach(purchase => {
        const purchaseDate = new Date(purchase.date);
        const dateStr = purchaseDate.toISOString().split('T')[0];
        const dayData = last7Days.find(day => day.date === dateStr);
        if (dayData) {
            if (purchase.status === 'done') {
                dayData.successfulCount++;
                dayData.successfulAmount += purchase.amount || 0;
                dayData.successfulPurchases.push(purchase);
            } else {
                dayData.failedCount++;
                dayData.failedAmount += purchase.amount || 0;
                dayData.failedPurchases.push(purchase);
            }
        }
    });

    return last7Days;
}

function createAdvancedPurchaseChart(ctx, data) {
    const labels = data.map(item => item.label);
    const successfulCounts = data.map(item => item.successfulCount);
    const failedCounts = data.map(item => item.failedCount);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Successful',
                    data: successfulCounts,
                    backgroundColor: 'rgba(30, 203, 129, 0.8)',
                    borderColor: '#1ecb81',
                    borderWidth: 2,
                    borderRadius: 6,
                    borderSkipped: false,
                    hoverBackgroundColor: 'rgba(30, 203, 129, 0.9)',
                    hoverBorderColor: '#1ecb81'
                },
                {
                    label: 'Failed',
                    data: failedCounts,
                    backgroundColor: 'rgba(255, 77, 79, 0.8)',
                    borderColor: '#ff4d4f',
                    borderWidth: 2,
                    borderRadius: 6,
                    borderSkipped: false,
                    hoverBackgroundColor: 'rgba(255, 77, 79, 0.9)',
                    hoverBorderColor: '#ff4d4f'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            resizeDelay: 0,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    align: 'end',
                    labels: {
                        color: '#e6eaf0',
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(35, 43, 53, 0.95)',
                    titleColor: '#e6eaf0',
                    bodyColor: '#e6eaf0',
                    borderColor: '#00b3ff',
                    borderWidth: 2,
                    cornerRadius: 12,
                    displayColors: true,
                    titleFont: {
                        size: window.innerWidth <= 480 ? 12 : 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: window.innerWidth <= 480 ? 11 : 13
                    },
                    padding: window.innerWidth <= 480 ? 10 : 15,
                    callbacks: {
                        title: function(context) {
                            const dataIndex = context[0].dataIndex;
                            return data[dataIndex].fullDate;
                        },
                        label: function(context) {
                            const dataIndex = context.dataIndex;
                            const dayData = data[dataIndex];
                            const datasetLabel = context.dataset.label;

                            const lines = [];

                            if (datasetLabel === 'Successful' && dayData.successfulPurchases.length > 0) {
                                dayData.successfulPurchases.forEach(purchase => {
                                    lines.push(`${purchase.payer || 'Unknown'} - ${purchase.amount} $/T (Success)`);
                                });
                            } else if (datasetLabel === 'Failed' && dayData.failedPurchases.length > 0) {
                                dayData.failedPurchases.forEach(purchase => {
                                    lines.push(`${purchase.payer || 'Unknown'} - ${purchase.amount} $/T (Failed)`);
                                });
                            }

                            return lines;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        color: '#8a97a8',
                        font: {
                            size: window.innerWidth <= 480 ? 9 : 11
                        },
                        maxTicksLimit: window.innerWidth <= 480 ? 5 : 8
                    },
                    grid: {
                        color: 'rgba(138, 151, 168, 0.1)',
                        drawBorder: false
                    }
                },
                x: {
                    ticks: {
                        color: '#8a97a8',
                        font: {
                            size: window.innerWidth <= 480 ? 9 : 11
                        },
                        maxRotation: window.innerWidth <= 480 ? 45 : 0,
                        minRotation: window.innerWidth <= 480 ? 45 : 0
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function showEmptyPurchaseChart(ctx) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'Successful',
                    data: [0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(138, 151, 168, 0.3)',
                    borderColor: '#8a97a8',
                    borderWidth: 1,
                    borderRadius: 6,
                    borderSkipped: false
                },
                {
                    label: 'Failed',
                    data: [0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(138, 151, 168, 0.2)',
                    borderColor: '#8a97a8',
                    borderWidth: 1,
                    borderRadius: 6,
                    borderSkipped: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    align: 'end',
                    labels: {
                        color: '#8a97a8',
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(35, 43, 53, 0.95)',
                    titleColor: '#e6eaf0',
                    bodyColor: '#e6eaf0',
                    borderColor: '#8a97a8',
                    borderWidth: 2,
                    cornerRadius: 12,
                    displayColors: false,
                    callbacks: {
                        label: function() {
                            return 'No purchases yet';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        stepSize: 1,
                        color: '#8a97a8',
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(138, 151, 168, 0.1)',
                        drawBorder: false
                    }
                },
                x: {
                    ticks: {
                        color: '#8a97a8',
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function updateLogs() {
    if (!dashboardData || !dashboardData.logs) return;

    const logsContainer = document.getElementById('logsBlur');
    if (!logsContainer) return;

    logsContainer.innerHTML = '';
    dashboardData.logs.forEach(log => {
        const logLine = document.createElement('div');
        logLine.className = 'log-line';
        logLine.textContent = log;
        logsContainer.appendChild(logLine);
    });
}

// Show logs functionality
function initializeLogsToggle() {
    const showLogsBtn = document.getElementById('showLogsBtn');
    const logsBlur = document.getElementById('logsBlur');
    const logCenterWrapper = document.getElementById('logCenterWrapper');

    if (showLogsBtn) {
        showLogsBtn.addEventListener('click', function() {
            if (logsBlur) {
                logsBlur.classList.add('active');
            }
            this.style.display = 'none';
            if (logCenterWrapper) {
                logCenterWrapper.style.display = 'none';
            }
        });
    }
}

function showError(message) {
    console.error(message);
}

function initializeSponsorContent() {
    const contents = document.querySelectorAll('.sponsor-content');
    const controls = document.querySelectorAll('.control-btn');
    let currentIndex = 0;

    if (contents.length === 0 || controls.length === 0) return;

    function showContent(index) {
        contents.forEach(content => content.classList.remove('active'));
        controls.forEach(btn => btn.classList.remove('active'));

        if (contents[index]) {
            contents[index].classList.add('active');
        }
        if (controls[index]) {
            controls[index].classList.add('active');
        }
        currentIndex = index;
    }

    setInterval(() => {
        const nextIndex = (currentIndex + 1) % contents.length;
        showContent(nextIndex);
    }, 5000);

    controls.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            showContent(index);
        });
    });

    showContent(0);
}

function handleChartResize() {
    const chart = Chart.getChart('purchaseChart');
    if (chart) {
        setTimeout(() => {
            chart.resize();
        }, 100);
    }
}

// Initialize dashboard
function initializeDashboard() {
    fetchGitHubStars();
    fetchDashboardData();
    initializeLogsToggle();
    initializeSponsorContent();

    window.addEventListener('resize', handleChartResize);
}

document.addEventListener('DOMContentLoaded', initializeDashboard);

// Refresh data every 30 seconds
setInterval(fetchDashboardData, 30000);
