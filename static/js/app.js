/**
 * Time and Task Manager - JavaScript Application
 * Handles timer updates, interactive features, and API calls
 */


// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Initialize mobile navigation
    initializeMobileNavigation();
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.container');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
}


/**
 * Format duration in seconds to human readable format
 */
function formatDuration(seconds) {
    if (seconds === 0) return "0m";
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (hours > 0) {
        return `${hours}h ${minutes}m`;
    } else {
        return `${minutes}m`;
    }
}

/**
 * Format datetime for display
 */
function formatDateTime(dateString) {
    try {
        const date = new Date(dateString);
        return date.toLocaleString();
    } catch (e) {
        return dateString;
    }
}

/**
 * Show loading state for an element
 */
function showLoading(element) {
    element.classList.add('loading');
    const originalText = element.textContent;
    element.setAttribute('data-original-text', originalText);
    
    if (element.tagName === 'BUTTON') {
        element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Loading...';
        element.disabled = true;
    }
}

/**
 * Hide loading state for an element
 */
function hideLoading(element) {
    element.classList.remove('loading');
    const originalText = element.getAttribute('data-original-text');
    
    if (element.tagName === 'BUTTON') {
        element.innerHTML = originalText;
        element.disabled = false;
        element.removeAttribute('data-original-text');
    }
}

/**
 * Show a toast notification (if Bootstrap toast is available)
 */
function showToast(message, type = 'info') {
    // Create toast element
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Find or create toast container
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Add toast to container
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Show toast
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.remove();
    });
}

/**
 * Confirm action with user
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Handle form submission with loading state
 */
function handleFormSubmission(form, button) {
    button.addEventListener('click', function(e) {
        const isValid = form.checkValidity();
        if (isValid) {
            showLoading(button);
        }
    });
}

/**
 * Auto-save functionality for forms
 */
function enableAutoSave(form, endpoint) {
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            // Debounce the save operation
            clearTimeout(input.saveTimeout);
            input.saveTimeout = setTimeout(() => {
                autoSaveForm(form, endpoint);
            }, 1000);
        });
    });
}

/**
 * Auto-save form data
 */
function autoSaveForm(form, endpoint) {
    const formData = new FormData(form);
    
    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Changes saved automatically', 'success');
        }
    })
    .catch(error => {
        console.log('Auto-save failed:', error);
    });
}

/**
 * Initialize tooltips for dynamically added content
 */
function initTooltips(container = document) {
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(container.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Utility function to get CSRF token if needed
 */
function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : null;
}

/**
 * Make API request with proper headers
 */
function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    const csrfToken = getCSRFToken();
    if (csrfToken) {
        defaultOptions.headers['X-CSRFToken'] = csrfToken;
    }
    
    return fetch(url, { ...defaultOptions, ...options });
}

/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N: New task
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        const newTaskLink = document.querySelector('a[href*="create"]');
        if (newTaskLink) {
            window.location.href = newTaskLink.href;
        }
    }
    
    // Ctrl/Cmd + T: Tasks page
    if ((e.ctrlKey || e.metaKey) && e.key === 't') {
        e.preventDefault();
        const tasksLink = document.querySelector('a[href*="tasks"]');
        if (tasksLink) {
            window.location.href = tasksLink.href;
        }
    }
    
    // Escape: Close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

/**
 * Initialize mobile navigation functionality
 */
function initializeMobileNavigation() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    if (!sidebarToggle || !sidebar || !backdrop) {
        return; // Elements not found, skip initialization
    }
    
    // Toggle sidebar when hamburger is clicked
    sidebarToggle.addEventListener('click', function(e) {
        e.preventDefault();
        toggleSidebar();
    });
    
    // Close sidebar when backdrop is clicked
    backdrop.addEventListener('click', function() {
        closeSidebar();
    });
    
    // Close sidebar when nav link is clicked (mobile)
    const navLinks = sidebar.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Only close on mobile
            if (window.innerWidth < 768) {
                closeSidebar();
            }
        });
    });
    
    // Close sidebar on window resize if desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            closeSidebar();
        }
    });
    
    // Close sidebar on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSidebar();
        }
    });
}

/**
 * Toggle mobile sidebar
 */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    if (sidebar.classList.contains('show')) {
        closeSidebar();
    } else {
        openSidebar();
    }
}

/**
 * Open mobile sidebar
 */
function openSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    sidebar.classList.add('show');
    backdrop.classList.add('show');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

/**
 * Close mobile sidebar
 */
function closeSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    sidebar.classList.remove('show');
    backdrop.classList.remove('show');
    document.body.style.overflow = ''; // Restore scrolling
}

/**
 * Export functions for use in other scripts
 */
window.TaskManager = {
    formatDuration,
    formatDateTime,
    showLoading,
    hideLoading,
    showToast,
    confirmAction,
    apiRequest,
    toggleSidebar,
    openSidebar,
    closeSidebar
};
