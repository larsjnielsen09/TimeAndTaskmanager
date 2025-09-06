/**
 * Time and Task Manager - JavaScript Application
 * Handles timer updates, interactive features, and API calls
 */

// Global timer state
let timerInterval = null;
let timerStartTime = null;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Check for active timer and update navbar indicator
    updateTimerStatus();
    
    // Set up periodic timer status updates
    setInterval(updateTimerStatus, 5000); // Check every 5 seconds
    
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
 * Update timer status in the navbar
 */
function updateTimerStatus() {
    fetch('/api/timer/status')
        .then(response => response.json())
        .then(data => {
            const timerIndicator = document.getElementById('timer-indicator');
            const timerText = document.getElementById('timer-text');
            
            if (data.active) {
                // Show timer indicator
                if (timerIndicator) {
                    timerIndicator.style.display = 'block';
                    timerStartTime = new Date(data.start_time);
                    startTimerDisplay();
                }
            } else {
                // Hide timer indicator
                if (timerIndicator) {
                    timerIndicator.style.display = 'none';
                    stopTimerDisplay();
                }
            }
        })
        .catch(error => {
            console.log('Timer status check failed:', error);
        });
}

/**
 * Start the timer display update
 */
function startTimerDisplay() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    timerInterval = setInterval(updateTimerDisplay, 1000);
    updateTimerDisplay(); // Update immediately
}

/**
 * Stop the timer display update
 */
function stopTimerDisplay() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

/**
 * Update the timer display
 */
function updateTimerDisplay() {
    if (!timerStartTime) return;
    
    const now = new Date();
    const elapsed = Math.floor((now - timerStartTime) / 1000);
    
    const hours = Math.floor(elapsed / 3600);
    const minutes = Math.floor((elapsed % 3600) / 60);
    const seconds = elapsed % 60;
    
    const display = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    const timerText = document.getElementById('timer-text');
    if (timerText) {
        timerText.textContent = display;
    }
    
    // Also update any active timer displays on the current page
    const activeTimerDisplays = document.querySelectorAll('#active-timer-display');
    activeTimerDisplays.forEach(element => {
        element.textContent = display;
    });
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
    
    // Ctrl/Cmd + T: Timer page
    if ((e.ctrlKey || e.metaKey) && e.key === 't') {
        e.preventDefault();
        const timerLink = document.querySelector('a[href*="timer"]');
        if (timerLink) {
            window.location.href = timerLink.href;
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
 * Export functions for use in other scripts
 */
window.TaskManager = {
    updateTimerStatus,
    formatDuration,
    formatDateTime,
    showLoading,
    hideLoading,
    showToast,
    confirmAction,
    apiRequest
};
