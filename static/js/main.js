// Mobile Landing Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initFileUploads();
    initFormValidation();
    initScrollAnimations();
    initCarousel();
    
    console.log('Mobile landing page initialized');
});

// File Upload Functionality
function initFileUploads() {
    const fileInputs = document.querySelectorAll('.file-input');
    
    fileInputs.forEach(input => {
        const container = input.closest('.file-input-container');
        const overlay = container.querySelector('.file-input-overlay');
        
        // Handle file selection
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                updateFileDisplay(container, overlay, file);
            }
        });
        
        // Handle click on overlay
        overlay.addEventListener('click', function() {
            input.click();
        });
        
        // Handle drag and drop
        overlay.addEventListener('dragover', function(e) {
            e.preventDefault();
            container.classList.add('drag-over');
        });
        
        overlay.addEventListener('dragleave', function(e) {
            e.preventDefault();
            container.classList.remove('drag-over');
        });
        
        overlay.addEventListener('drop', function(e) {
            e.preventDefault();
            container.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                updateFileDisplay(container, overlay, files[0]);
            }
        });
    });
}

// Update file display after selection
function updateFileDisplay(container, overlay, file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (file.size > maxSize) {
        showError('Файл слишком большой. Максимальный размер: 16MB');
        return;
    }
    
    container.classList.add('has-file');
    
    // Create file info display
    const fileName = file.name.length > 30 ? 
        file.name.substring(0, 30) + '...' : file.name;
    const fileSize = formatFileSize(file.size);
    
    overlay.innerHTML = `
        <div class="file-selected">
            <i class="fas fa-check-circle text-success me-2"></i>
            <div>
                <div class="fw-bold">${fileName}</div>
                <div class="small text-muted">${fileSize}</div>
            </div>
        </div>
    `;
    
    // Add remove button
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'btn btn-sm btn-outline-danger ms-2';
    removeBtn.innerHTML = '<i class="fas fa-times"></i>';
    removeBtn.onclick = function(e) {
        e.stopPropagation();
        clearFileInput(container, overlay);
    };
    
    overlay.querySelector('.file-selected').appendChild(removeBtn);
}

// Clear file input
function clearFileInput(container, overlay) {
    const input = container.querySelector('.file-input');
    input.value = '';
    container.classList.remove('has-file');
    
    overlay.innerHTML = `
        <i class="fas fa-camera me-2"></i>Выбрать файл или сфотографировать
    `;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form Validation
function initFormValidation() {
    const form = document.getElementById('uploadForm');
    if (!form) return;
    
    const submitBtn = document.getElementById('submitBtn');
    
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Загрузка...';
        submitBtn.disabled = true;
        
        // Add loading class to form
        form.classList.add('loading');
    });
}

// Validate form
function validateForm() {
    let isValid = true;
    const requiredFields = document.querySelectorAll('.form-control[required], .file-input[required]');
    
    requiredFields.forEach(field => {
        if (!field.value || (field.type === 'file' && !field.files.length)) {
            markFieldInvalid(field);
            isValid = false;
        } else {
            markFieldValid(field);
        }
    });
    
    // Validate email format
    const emailField = document.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
            markFieldInvalid(emailField);
            isValid = false;
        }
    }
    
    // Validate phone format
    const phoneField = document.querySelector('input[name="phone"]');
    if (phoneField && phoneField.value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(phoneField.value.replace(/\s+/g, ''))) {
            markFieldInvalid(phoneField);
            isValid = false;
        }
    }
    
    if (!isValid) {
        showError('Пожалуйста, заполните все обязательные поля корректно');
        scrollToFirstError();
    }
    
    return isValid;
}

// Mark field as invalid
function markFieldInvalid(field) {
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
}

// Mark field as valid
function markFieldValid(field) {
    field.classList.add('is-valid');
    field.classList.remove('is-invalid');
}

// Scroll to first error
function scrollToFirstError() {
    const firstError = document.querySelector('.is-invalid');
    if (firstError) {
        firstError.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
        firstError.focus();
    }
}

// Show error message
function showError(message) {
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.error-message');
    existingErrors.forEach(error => error.remove());
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger error-message fade-in';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Insert at top of form
    const form = document.getElementById('uploadForm');
    if (form) {
        form.insertBefore(errorDiv, form.firstChild);
    }
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll(
        '.welcome-message, .cta-content, .form-section'
    );
    
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}

// Carousel Functionality
function initCarousel() {
    const carousel = document.getElementById('logoCarousel');
    if (!carousel) return;
    
    // Pause animation on hover
    carousel.addEventListener('mouseenter', function() {
        this.style.animationPlayState = 'paused';
    });
    
    carousel.addEventListener('mouseleave', function() {
        this.style.animationPlayState = 'running';
    });
    
    // Touch/swipe support for mobile
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    carousel.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        isDragging = true;
        this.style.animationPlayState = 'paused';
    });
    
    carousel.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        currentX = e.touches[0].clientX;
        const diff = startX - currentX;
        // Optional: Add manual scrolling logic here
    });
    
    carousel.addEventListener('touchend', function() {
        isDragging = false;
        this.style.animationPlayState = 'running';
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Input formatting
document.addEventListener('input', function(e) {
    if (e.target.name === 'phone') {
        formatPhoneInput(e.target);
    }
});

function formatPhoneInput(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length >= 10) {
        if (value.startsWith('1')) {
            value = `+1 (${value.slice(1, 4)}) ${value.slice(4, 7)}-${value.slice(7, 11)}`;
        } else {
            value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
        }
    }
    
    input.value = value;
}

// Handle network errors
window.addEventListener('online', function() {
    showSuccessMessage('Соединение восстановлено');
});

window.addEventListener('offline', function() {
    showError('Нет соединения с интернетом. Проверьте подключение.');
});

function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success fade-in';
    successDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
    `;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        if (successDiv.parentElement) {
            successDiv.remove();
        }
    }, 3000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
