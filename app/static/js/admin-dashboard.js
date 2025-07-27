
function initializeMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    if (!sidebar || !mobileMenuToggle || !sidebarOverlay) return;

    mobileMenuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        sidebarOverlay.classList.toggle('active');
    });

    sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 1024) {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
        }
    });
}

// Fetch dashboard data
async function fetchDashboardData() {
    try {
        const dashboardResponse = await fetch('/admin-dashboard/dashboard-data', {
            credentials: 'include'
        });

        if (!dashboardResponse.ok) {
            if (dashboardResponse.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to fetch dashboard data');
        }

        const dashboardData = await dashboardResponse.json();

        // Update stats
        updateStatCard('totalUsers', dashboardData.totalClients || 0);
        updateStatCard('availableData', dashboardData.availableDataGB || 0);
        updateStatCard('daysRemaining', dashboardData.daysRemaining || 0);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load dashboard data');
    }
}

// Fetch and display dashboard statistics
async function fetchStats() {
    try {
        const response = await fetch('/admin-dashboard/stats', {
            method: 'GET',
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch stats');
        }
        
        const data = await response.json();
        
        updateStatCard('totalUsers', data.total_users || 0);
        updateStatCard('activeUsers', data.active_users || 0);
        updateStatCard('totalTraffic', formatBytes(data.total_traffic || 0));
        updateStatCard('usedTraffic', formatBytes(data.used_traffic || 0));
        
    } catch (error) {
        console.error('Error fetching stats:', error);
        updateStatCard('totalUsers', 'Error');
        updateStatCard('activeUsers', 'Error');
        updateStatCard('totalTraffic', 'Error');
        updateStatCard('usedTraffic', 'Error');
    }
}

function updateStatCard(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = value;
        
        element.classList.add('stat-updated');
        setTimeout(() => {
            element.classList.remove('stat-updated');
        }, 500);
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Auto-refresh stats every 30 seconds
function startStatsAutoRefresh() {
    setInterval(() => {
        fetchStats();
    }, 30 * 1000); // 30 seconds
}

function initializeDashboard() {
    initializeMobileMenu();

    fetchDashboardData();

    fetchStats();

    startStatsAutoRefresh();

    if (window.adminNews) {
        window.adminNews.init();
        window.adminNews.startAutoRefresh();
    }

    addStatCardEffects();
}

function addStatCardEffects() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('stat-card-hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('stat-card-hover');
        });
        
        card.addEventListener('click', function() {
            this.classList.add('stat-card-clicked');
            setTimeout(() => {
                this.classList.remove('stat-card-clicked');
            }, 200);
        });
    });
}

window.adminDashboard = {
    fetchStats: fetchStats,
    init: initializeDashboard,
    formatBytes: formatBytes
};

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});
