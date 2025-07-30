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
        const username = fileName.split('_')[0];
        return `
            <div class=\"receipt-card\">\n                <div class=\"receipt-image-container\">\n                    <img src=\"${imageUrl}\" alt=\"Receipt\" class=\"receipt-image\" onclick=\"openImageModal('${imageUrl}', '${fileName}')\">\n                    <div class=\"receipt-overlay\">\n                        <div class=\"receipt-actions\">\n                            <button class=\"receipt-btn\" onclick=\"openImageModal('${imageUrl}', '${fileName}')\">\n                                <i class=\"fas fa-eye\"></i>\n                            </button>\n                        </div>\n                    </div>\n                </div>\n                <div class=\"receipt-info\">\n                    <div class=\"receipt-username\">\n                        <span style=\"color:#fff;font-weight:bold;\">Admin:</span> <span style=\"color:#bdbdbd;font-weight:bold;\">${username}</span>\n                    </div>\n                    <div class=\"receipt-name\" style=\"color:#bdbdbd;\">${fileName}</div>\n                </div>\n            </div>\n        `;
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
function openImageModal(imageUrl, fileName) {
    // Remove any existing modal
    document.querySelectorAll('.modal.active').forEach(m => m.remove());
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.style.zIndex = '3000';
    modal.innerHTML = `
        <div class="modal-content">
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
                <img src="${imageUrl}" alt="Receipt">
                <div class="receipt-name" style="margin: 8px 0;">${fileName}</div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-outline" onclick="this.closest('.modal').remove()">Cancel</button>
                <button class="btn btn-danger" onclick="modalDeleteReceipt('${fileName}', this)">Reject</button>
                <button class="btn btn-success" onclick="modalApproveReceipt('${fileName}', this)">Approve</button>
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

// Utility function to remove file extension
function getImageNameWithoutExtension(filename) {
    return filename.replace(/\.[^/.]+$/, "");
}

// Add approveReceipt function
async function approveReceipt(fileName) {
    const imageName = getImageNameWithoutExtension(fileName);
    try {
        const response = await fetch(`/payment/aproval-payment/${imageName}`, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to approve receipt');
        }
        const result = await response.json();
        if (result.status) {
            showMessage('Receipt approved successfully', 'success');
            loadReceipts();
        } else {
            showMessage(result.message || 'Failed to approve receipt', 'error');
        }
    } catch (error) {
        console.error('Error approving receipt:', error);
        showMessage('Failed to approve receipt', 'error');
    }
}

// Modal Approve functions
async function modalApproveReceipt(fileName, btn) {
    btn.disabled = true;
    try {
        const response = await fetch(`/payment/aproval-payment/${fileName}`, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to approve receipt');
        }
        const result = await response.json();
        showToast(result.message, result.status ? 'success' : 'error');
        if (result.status) {
            setTimeout(() => {
                loadReceipts();
            }, 1000);
        }
    } catch (error) {
        console.error('Error approving receipt:', error);
        showToast('Failed to approve receipt', 'error');
    }
    document.querySelectorAll('.modal.active').forEach(m => m.remove());
}

async function modalDeleteReceipt(fileName, btn) {
    btn.disabled = true;
    try {
        const response = await fetch(`/payment/delete-receipt-image/${fileName}`, {
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
            showMessage('Receipt deleted successfully', 'success');
            loadReceipts();
        } else {
            showMessage(result.message || 'Failed to delete receipt', 'error');
        }
    } catch (error) {
        console.error('Error deleting receipt:', error);
        showMessage('Failed to delete receipt', 'error');
    }
    document.querySelectorAll('.modal.active').forEach(m => m.remove());
}

function showToast(message, type) {
    const toast = document.getElementById('toast-message');
    toast.textContent = message;
    toast.style.background = type === 'success' ? '#4caf50' : '#f44336';
    toast.style.display = 'block';
    clearTimeout(window.toastTimeout);
    window.toastTimeout = setTimeout(() => {
        toast.style.display = 'none';
    }, 2500);
}

async function approvePayment(imageName) {
    try {
        const response = await fetch(`/payment/aproval-payment/${imageName}`);
        const data = await response.json();
        showToast(data.message, data.status ? 'success' : 'error');
    } catch (error) {
        showToast('Server error', 'error');
    }
} 