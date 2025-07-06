// Receipts Page JavaScript
let currentReceiptToDelete = null;

// Mobile menu functionality
const sidebar = document.getElementById('sidebar');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebarOverlay = document.getElementById('sidebarOverlay');

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

// Load receipts on page load
document.addEventListener('DOMContentLoaded', () => {
    loadReceipts();
});

// Function to load receipts
async function loadReceipts() {
    const receiptsGrid = document.getElementById('receiptsGrid');
    const emptyState = document.getElementById('emptyState');
    
    // Show loading state
    receiptsGrid.innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner"></i>
            Loading receipts...
        </div>
    `;
    
    try {
        const response = await fetch('/payment/get-receipt-image', {
            credentials: 'include'
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to fetch receipts');
        }
        
        const data = await response.json();
        const images = data.images || [];
        
        if (images.length === 0) {
            receiptsGrid.style.display = 'none';
            emptyState.style.display = 'block';
        } else {
            receiptsGrid.style.display = 'grid';
            emptyState.style.display = 'none';
            displayReceipts(images);
        }
        
    } catch (error) {
        console.error('Error loading receipts:', error);
        receiptsGrid.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Error Loading Receipts</h3>
                <p>Failed to load receipt images. Please try again.</p>
            </div>
        `;
    }
}

// Function to display receipts in grid
function displayReceipts(images) {
    const receiptsGrid = document.getElementById('receiptsGrid');
    
    receiptsGrid.innerHTML = images.map(imageUrl => {
        const fileName = imageUrl.split('/').pop();
        const fileDate = getFileDate(fileName);
        
        return `
            <div class="receipt-card">
                <div class="receipt-image-container">
                    <img src="${imageUrl}" alt="Receipt" class="receipt-image" onclick="openImageModal('${imageUrl}')">
                    <div class="receipt-overlay">
                        <div class="receipt-actions">
                            <button class="receipt-btn" onclick="openImageModal('${imageUrl}')">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="receipt-btn danger" onclick="showDeleteModal('${fileName}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="receipt-info">
                    <div class="receipt-name">${fileName}</div>
                    <div class="receipt-date">${fileDate}</div>
                </div>
            </div>
        `;
    }).join('');
}

// Function to get file date (extract from filename or use current date)
function getFileDate(fileName) {
    // Try to extract date from filename if it contains date pattern
    const dateMatch = fileName.match(/(\d{4})-(\d{2})-(\d{2})/);
    if (dateMatch) {
        const [_, year, month, day] = dateMatch;
        return `${year}-${month}-${day}`;
    }
    
    // If no date in filename, use current date
    const now = new Date();
    return now.toISOString().split('T')[0];
}

// Function to open image in modal
function openImageModal(imageUrl) {
    // Create a simple modal to show the full image
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.style.zIndex = '3000';
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 90%; max-height: 90%;">
            <div class="modal-header">
                <h3 class="modal-title">
                    <i class="fas fa-image"></i>
                    Receipt Image
                </h3>
                <button class="close-modal" onclick="this.closest('.modal').remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body" style="text-align: center; padding: 0;">
                <img src="${imageUrl}" alt="Receipt" style="max-width: 100%; max-height: 70vh; object-fit: contain;">
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// Function to show delete confirmation modal
function showDeleteModal(fileName) {
    currentReceiptToDelete = fileName;
    const modal = document.getElementById('deleteModal');
    const receiptNameElement = document.getElementById('receiptName');
    
    receiptNameElement.textContent = fileName;
    modal.classList.add('active');
}

// Function to close delete modal
function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('active');
    currentReceiptToDelete = null;
}

// Function to confirm delete
async function confirmDelete() {
    if (!currentReceiptToDelete) return;
    
    try {
        const response = await fetch(`/payment/delete-receipt-image/${currentReceiptToDelete}`, {
            method: 'GET',
            credentials: 'include'
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to delete receipt');
        }
        
        const result = await response.json();
        
        if (result.status) {
            // Show success message
            showMessage('Receipt deleted successfully', 'success');
            // Reload receipts
            loadReceipts();
        } else {
            showMessage(result.message || 'Failed to delete receipt', 'error');
        }
        
    } catch (error) {
        console.error('Error deleting receipt:', error);
        showMessage('Failed to delete receipt', 'error');
    }
    
    closeDeleteModal();
}

// Function to refresh receipts
function refreshReceipts() {
    loadReceipts();
}

// Function to show messages
function showMessage(message, type = 'info') {
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = `message ${type}`;
    messageElement.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    document.body.appendChild(messageElement);
    
    // Show message
    setTimeout(() => {
        messageElement.style.opacity = '1';
        messageElement.style.transform = 'translateY(0)';
    }, 100);
    
    // Remove message after 3 seconds
    setTimeout(() => {
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(-100%)';
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 300);
    }, 3000);
}

// Close modal when pressing Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDeleteModal();
    }
}); 