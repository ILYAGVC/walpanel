// Fetch and display news for admins
async function fetchAdminNews() {
    const newsList = document.getElementById('newsList');
    const newsCount = document.getElementById('newsCount');
    const newsSection = document.querySelector('.news-section');
    
    if (!newsList) return;
    
    newsList.innerHTML = '<div class="news-loading"><i class="fas fa-spinner fa-spin"></i> Loading news...</div>';
    
    try {
        const response = await fetch('/admin-dashboard/news', { credentials: 'include' });
        if (!response.ok) throw new Error('Failed to fetch news');
        const news = await response.json();
        
        if (!news || news.length === 0) {
            newsList.innerHTML = `
                <div class="news-empty">
                    <i class="fas fa-inbox"></i>
                    <p>No news available</p>
                </div>
            `;
            newsCount.textContent = '0';
            return;
        }
        
        newsCount.textContent = news.length;
        newsList.innerHTML = news.map((item, index) => `
            <div class="news-item" data-index="${index}">
                <div class="news-item-header">
                    <div class="news-item-icon">
                        <i class="fas fa-bullhorn"></i>
                    </div>
                    <div class="news-item-meta">
                        <span class="news-item-type">Announcement</span>
                        <span class="news-item-time">${formatTimeAgo(new Date())}</span>
                    </div>
                </div>
                <div class="news-item-content">
                    <p>${item.message}</p>
                </div>
                <div class="news-item-footer">
                    <span class="news-item-status">New</span>
                </div>
            </div>
        `).join('');
        
        document.querySelectorAll('.news-item').forEach(item => {
            item.addEventListener('click', function() {
                this.classList.add('news-item-clicked');
                setTimeout(() => this.classList.remove('news-item-clicked'), 200);
            });
        });
        
    } catch (error) {
        newsList.innerHTML = `
            <div class="news-error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>${error.message}</p>
            </div>
        `;
        newsCount.textContent = '!';
    }
}

function toggleNewsSection() {
    const newsContainer = document.getElementById('newsList');
    const toggleBtn = document.querySelector('.news-toggle-btn');
    const toggleIcon = toggleBtn.querySelector('i');
    
    if (newsContainer.style.display === 'none') {
        // Show news
        newsContainer.style.display = 'flex';
        toggleIcon.className = 'fas fa-chevron-up';
        toggleBtn.setAttribute('aria-expanded', 'true');
        newsContainer.classList.add('news-expanding');
        setTimeout(() => newsContainer.classList.remove('news-expanding'), 300);
    } else {
        // Hide news
        newsContainer.style.display = 'none';
        toggleIcon.className = 'fas fa-chevron-down';
        toggleBtn.setAttribute('aria-expanded', 'false');
    }
}

function formatTimeAgo(date) {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    return `${Math.floor(diffInSeconds / 86400)}d ago`;
}

function initializeNewsSection() {
    const toggleBtn = document.querySelector('.news-toggle-btn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleNewsSection);
    }

    const newsContainer = document.getElementById('newsList');
    const toggleIcon = toggleBtn.querySelector('i');
    if (newsContainer && toggleIcon) {
        newsContainer.style.display = 'none';
        toggleIcon.className = 'fas fa-chevron-down';
        toggleBtn.setAttribute('aria-expanded', 'false');
    }

    // Fetch news
    fetchAdminNews();
}

// Auto-refresh news every 5 minutes
function startNewsAutoRefresh() {
    setInterval(() => {
        const newsContainer = document.getElementById('newsList');

        if (newsContainer && newsContainer.style.display !== 'none') {
            fetchAdminNews();
        }
    }, 5 * 60 * 1000); // 5 minutes
}

window.adminNews = {
    fetch: fetchAdminNews,
    toggle: toggleNewsSection,
    init: initializeNewsSection,
    startAutoRefresh: startNewsAutoRefresh
};
