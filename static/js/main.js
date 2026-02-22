/*
SmartCater - Advanced JavaScript
Enhances UI with animations, transitions, and interactivity
*/

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // NAVBAR SCROLL EFFECT
    // ========================================
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // ========================================
    // STAGGERED ANIMATION ON PAGE LOAD
    // ========================================
    const animateElements = document.querySelectorAll('.animate-on-load');
    
    animateElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // ========================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ========================================
    // ENHANCED FORM VALIDATION
    // ========================================
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // ========================================
    // TOAST NOTIFICATIONS
    // ========================================
    function showToast(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container');
        
        if (!toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">SmartCater</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }
    
    // ========================================
    // CARD HOVER EFFECTS
    // ========================================
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // ========================================
    // BUTTON LOADING STATE
    // ========================================
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                this.innerHTML = '<span class="loading"></span> Processing...';
                this.disabled = true;
                
                setTimeout(() => {
                    this.innerHTML = 'Processing...';
                }, 2000);
            }
        });
    });
    
    // ========================================
    // PARALLAX EFFECT FOR HERO
    // ========================================
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            
            heroSection.style.backgroundPositionY = rate + 'px';
        });
    }
    
    // ========================================
    // LAZY LOADING IMAGES
    // ========================================
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => {
        imageObserver.observe(img);
    });
    
    // ========================================
    // COUNTER ANIMATION
    // ========================================
    const counters = document.querySelectorAll('.counter');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.dataset.target);
                const duration = 2000;
                const increment = target / (duration / 16);
                
                let current = 0;
                
                const updateCounter = () => {
                    current += increment;
                    
                    if (current < target) {
                        counter.innerText = Math.ceil(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.innerText = target;
                    }
                };
                
                updateCounter();
                counterObserver.unobserve(counter);
            }
        });
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
    
    // ========================================
    // SKELETON LOADING EFFECT
    // ========================================
    const skeletons = document.querySelectorAll('.skeleton');
    
    skeletons.forEach(skeleton => {
        skeleton.classList.add('loaded');
    });
    
    // ========================================
    // DROPDOWN MENU ANIMATION
    // ========================================
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('show.bs.dropdown', function() {
            this.querySelector('.dropdown-menu').style.opacity = '0';
            this.querySelector('.dropdown-menu').style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                this.querySelector('.dropdown-menu').style.transition = 'all 0.3s ease';
                this.querySelector('.dropdown-menu').style.opacity = '1';
                this.querySelector('.dropdown-menu').style.transform = 'translateY(0)';
            }, 10);
        });
    });
    
    // ========================================
    // MODAL ENHANCEMENTS
    // ========================================
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            this.querySelector('.modal-content').style.opacity = '0';
            this.querySelector('.modal-content').style.transform = 'scale(0.9)';
            
            setTimeout(() => {
                this.querySelector('.modal-content').style.transition = 'all 0.3s ease';
                this.querySelector('.modal-content').style.opacity = '1';
                this.querySelector('.modal-content').style.transform = 'scale(1)';
            }, 10);
        });
    });
    
    // ========================================
    // PROGRESS BAR ANIMATION
    // ========================================
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        
        setTimeout(() => {
            bar.style.transition = 'width 1s ease';
            bar.style.width = width;
        }, 100);
    });
    
    // ========================================
    // SCROLL REVEAL ANIMATION
    // ========================================
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, {
        threshold: 0.1
    });
    
    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
    
    // ========================================
    // MOBILE MENU TOGGLE ANIMATION
    // ========================================
    const navbarToggler = document.querySelector('.navbar-toggler');
    
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }
    
    // ========================================
    // CUSTOM CURSOR (OPTIONAL)
    // ========================================
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);
    
    document.addEventListener('mousemove', function(e) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });
    
    // ========================================
    // KEYBOARD SHORTCUTS
    // ========================================
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Home - Go to home
        if ((e.ctrlKey || e.metaKey) && e.key === 'Home') {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Ctrl/Cmd + K - Search focus
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
    
    // ========================================
    // PREVENT ACCIDENTAL NAVIGATION
    // ========================================
    const formsWithUnsavedChanges = document.querySelectorAll('form[data-unsafe]');
    
    formsWithUnsavedChanges.forEach(form => {
        form.addEventListener('change', function() {
            window.onbeforeunload = function() {
                return 'You have unsaved changes. Are you sure you want to leave?';
            };
        });
        
        form.addEventListener('submit', function() {
            window.onbeforeunload = null;
        });
    });
    
    // ========================================
    // AUTO-SAVE INDICATOR
    // ========================================
    const autoSaveElements = document.querySelectorAll('[data-autosave]');
    
    autoSaveElements.forEach(element => {
        let timeout;
        
        element.addEventListener('input', function() {
            const indicator = this.parentElement.querySelector('.save-indicator');
            
            if (indicator) {
                indicator.innerHTML = '<span class="loading"></span> Saving...';
            }
            
            clearTimeout(timeout);
            
            timeout = setTimeout(() => {
                if (indicator) {
                    indicator.innerHTML = '<i class="fas fa-check text-success"></i> Saved';
                    
                    setTimeout(() => {
                        indicator.innerHTML = '';
                    }, 2000);
                }
            }, 1000);
        });
    });
    
    // ========================================
    // TOGGLE PASSWORD VISIBILITY
    // ========================================
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    });
    
    // ========================================
    // INFINITE SCROLL (FOR LISTS)
    // ========================================
    const infiniteScrollContainers = document.querySelectorAll('[data-infinite-scroll]');
    
    infiniteScrollContainers.forEach(container => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Trigger load more event
                    container.dispatchEvent(new Event('loadMore'));
                }
            });
        });
        
        observer.observe(container);
    });
    
    // ========================================
    // INITIALIZE AOS-LIKE ANIMATIONS
    // ========================================
    const animatedElements = document.querySelectorAll('[data-aos]');
    
    const aosObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const animation = entry.target.dataset.aos;
                entry.target.classList.add('aos-' + animation);
                entry.target.classList.add('aos-animate');
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(el => {
        aosObserver.observe(el);
    });
    
});

// ========================================
// ADDITIONAL UTILITY FUNCTIONS
// ========================================

// Format currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Format date
function formatDate(date, format = 'long') {
    const options = format === 'long' 
        ? { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
        : { year: 'numeric', month: 'short', day: 'numeric' };
    
    return new Date(date).toLocaleDateString('en-US', options);
}

// Debounce function
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

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Copy to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        });
    } else {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showNotification('Copied to clipboard!', 'success');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const container = document.querySelector('.notification-container');
    
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    container.appendChild(notification);
    
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.remove();
    });
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Export functions for use in other scripts
window.SmartCater = {
    formatCurrency,
    formatDate,
    debounce,
    throttle,
    copyToClipboard,
    showNotification
};
