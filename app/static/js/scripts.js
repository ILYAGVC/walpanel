// Mobile menu functionality
const sidebar = document.getElementById('sidebar');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const panelModal = document.getElementById('panelModal');
const panelForm = document.getElementById('panelForm');
const modalTitle = document.getElementById('modalTitle');
const addPanelBtn = document.getElementById('addPanelBtn');
const emptyAddPanelBtn = document.getElementById('emptyAddPanelBtn');
const formMessage = document.getElementById('formMessage');

// Toggle sidebar on mobile
mobileMenuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
    sidebarOverlay.classList.toggle('active');
});

// Close sidebar when clicking overlay
sidebarOverlay.addEventListener('click', () => {
    sidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
});

// Close sidebar when window is resized to desktop size
window.addEventListener('resize', () => {
    if (window.innerWidth > 1024) {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    }
});

// Show modal function
function showModal() {
    panelModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Hide modal function
function hideModal() {
    panelModal.classList.remove('active');
    document.body.style.overflow = '';
    panelForm.reset();
    formMessage.style.display = 'none';
}

// Edit panel function
function editPanel(panel) {
    document.getElementById('panelId').value = panel.id;
    document.getElementById('panelName').value = panel.name;
    document.getElementById('panelUrl').value = panel.url;
    document.getElementById('panelSub').value = panel.sub;
    document.getElementById('panelUsername').value = panel.username;
    document.getElementById('panelPassword').required = false;

    modalTitle.textContent = 'Edit Panel';
    panelForm.dataset.mode = 'edit';

    showModal();
}

// Add panel button click
addPanelBtn.addEventListener('click', () => {
    modalTitle.textContent = 'Add Panel';
    panelForm.dataset.mode = 'add';
    document.getElementById('panelPassword').required = true;
    showModal();
});

// Empty state add panel button
emptyAddPanelBtn?.addEventListener('click', () => {
    modalTitle.textContent = 'Add Panel';
    panelForm.dataset.mode = 'add';
    document.getElementById('panelPassword').required = true;
    showModal();
});

// Show message in form
function showMessage(message, type) {
    formMessage.textContent = message;
    formMessage.className = `message message-${type}`;
    formMessage.style.display = 'block';
}

// Get token from cookie
function getToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'access_token') {
            return value;
        }
    }
    return null;
}

// Form submission
panelForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        name: document.getElementById('panelName').value,
        url: document.getElementById('panelUrl').value,
        sub: document.getElementById('panelSub').value,
        username: document.getElementById('panelUsername').value
    };

    const password = document.getElementById('panelPassword').value;
    if (password) formData.password = password;

    const mode = panelForm.dataset.mode;
    const panelId = document.getElementById('panelId').value;

    try {
        let response;
        let url = '/panel/create';

        if (mode === 'edit') {
            url = `/panel/edit/${panelId}`;
        }

        const token = getToken();
        console.log('Using token:', token);

        response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to save panel');
        }

        showMessage(
            mode === 'edit'
                ? 'Panel updated successfully!'
                : 'Panel added successfully!',
            'success'
        );

        // Reload after 1 second
        setTimeout(() => {
            window.location.reload();
        }, 1000);

    } catch (error) {
        console.error('Error:', error);
        showMessage(error.message, 'error');
    }
});

// Delete confirmation
function confirmDelete(panelId) {
    if (confirm('Are you sure you want to delete this panel? This action cannot be undone.')) {
        deletePanel(panelId);
    }
}

// Delete panel function
async function deletePanel(panelId) {
    try {
        const token = getToken();
        console.log('Using token for delete:', token);

        const response = await fetch(`/panel/delete/${panelId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('Delete response status:', response.status);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete panel');
        }

        // Reload the page to see changes
        window.location.reload();

    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}

