// ===========================
// MODERN CAFEMATE SYSTEM - JAVASCRIPT
// ===========================

// Document Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCafeStatus();
    initializeSmoothScrolling();
    initializeAnimations();
    initializeMobileMenu();
    initializeDatePicker();
    removeAlerts();
});

// ===========================
// CAFE STATUS MANAGEMENT
// ===========================

function initializeCafeStatus() {
    updateCafeStatus();
    // Update status every minute
    setInterval(updateCafeStatus, 60000);
}

function updateCafeStatus() {
    const now = new Date();
    const currentTime = now.getHours() * 100 + now.getMinutes();
    const openingTime = 800; // 8:00 AM
    const closingTime = 2200; // 10:00 PM

    const statusElements = document.querySelectorAll('.cafe-status-badge, #footer-status');
    statusElements.forEach(element => {
        if (currentTime >= openingTime && currentTime <= closingTime) {
            element.textContent = 'Open Now';
            element.className = element.className.replace('badge-danger', 'badge-success');
            if (!element.className.includes('badge-success')) {
                element.className += ' badge-success';
            }
        } else {
            element.textContent = 'Closed';
            element.className = element.className.replace('badge-success', 'badge-danger');
            if (!element.className.includes('badge-danger')) {
                element.className += ' badge-danger';
            }
        }
    });
}

// ===========================
// SMOOTH SCROLLING
// ===========================

function initializeSmoothScrolling() {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.offsetTop;
                const offsetPosition = elementPosition - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===========================
// ANIMATIONS
// ===========================

function initializeAnimations() {
    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.menu-card, .gallery-item, .testimonial-card').forEach(el => {
        observer.observe(el);
    });
}

// ===========================
// MOBILE MENU
// ===========================

function initializeMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });

        // Close menu when clicking on a link
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', function() {
                navbarCollapse.classList.remove('show');
            });
        });
    }
}

// ===========================
// DATE PICKER (Legacy support)
// ===========================

function initializeDatePicker() {
    // This is kept for backward compatibility
    // Modern date picker is handled in individual templates
}

// ===========================
// UTILITY FUNCTIONS
// ===========================

function removeAlerts() {
    // Auto-remove alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

// ===========================
// GALLERY LIGHTBOX (Simple implementation)
// ===========================

function initializeGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');

    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img) {
                // Simple lightbox - could be enhanced with a proper lightbox library
                const lightbox = document.createElement('div');
                lightbox.style.cssText = `
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.8); display: flex; align-items: center;
                    justify-content: center; z-index: 9999; cursor: pointer;
                `;
                lightbox.innerHTML = `<img src="${img.src}" style="max-width: 90%; max-height: 90%; object-fit: contain;">`;
                lightbox.addEventListener('click', () => document.body.removeChild(lightbox));
                document.body.appendChild(lightbox);
            }
        });
    });
}

// ===========================
// FORM VALIDATION
// ===========================

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// ===========================
// LOADING STATES
// ===========================

function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    button.disabled = true;

    return () => {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// ===========================
// LOCAL STORAGE HELPERS
// ===========================

const Storage = {
    set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
    get: (key) => {
        try {
            return JSON.parse(localStorage.getItem(key));
        } catch {
            return null;
        }
    },
    remove: (key) => localStorage.removeItem(key)
};

// ===========================
// KEYBOARD SHORTCUTS
// ===========================

document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], #menuSearch');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Escape: Close modals/lightboxes
    if (e.key === 'Escape') {
        const lightbox = document.querySelector('[style*="position: fixed"]');
        if (lightbox) {
            lightbox.remove();
        }
    }
});

// ===========================
// PERFORMANCE OPTIMIZATIONS
// ===========================

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
lazyLoadImages();

// ===========================
// DARK MODE TOGGLE (Optional Feature)
// ===========================

function initializeDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (!darkModeToggle) return;

    // Check for saved theme preference
    const currentTheme = Storage.get('theme') || 'light';

    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }

    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            Storage.set('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            Storage.set('theme', 'light');
        }
    });
}

// Initialize dark mode if toggle exists
initializeDarkMode();
                menu.style.visibility = 'hidden';
            }
        });
    });
}

// ===========================
// DATE PICKER
// ===========================

function initializeDatePicker() {
    const dateInput = document.querySelector('input[type="date"]');
    
    if (dateInput) {
        // Set minimum date to today
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const minDate = `${year}-${month}-${day}`;
        
        dateInput.min = minDate;
        dateInput.value = minDate;
    }
}

// ===========================
// UPDATE CAFE STATUS
// ===========================

function updateCafeStatus() {
    const statusBar = document.querySelector('.status-bar');
    
    if (statusBar) {
        // Fetch status every minute
        fetchCafeStatus();
        setInterval(fetchCafeStatus, 60000);
    }
}

function fetchCafeStatus() {
    fetch('/api/cafe-timing/')
        .then(response => response.json())
        .then(data => {
            const statusBar = document.querySelector('.status-bar');
            const badge = document.querySelector('.status-badge');
            const timeSpan = document.querySelector('.status-time');
            
            if (badge) {
                badge.textContent = data.status;
                badge.className = 'status-badge status-' + (data.is_open ? 'open' : 'closed');
                badge.classList.add(data.is_open ? 'badge-open' : 'badge-closed');
            }
        })
        .catch(error => console.log('Error fetching cafe status:', error));
}

// ===========================
// SMOOTH SCROLL
// ===========================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
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

// ===========================
// ANIMATIONS
// ===========================

function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.menu-card, .info-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
}

// ===========================
// SEARCH MENU
// ===========================

const searchInput = document.querySelector('.menu-search');
if (searchInput) {
    let searchTimeout;
    
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            return;
        }
        
        searchTimeout = setTimeout(() => {
            fetch(`/api/search-menu/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    displaySearchResults(data.results);
                })
                .catch(error => console.log('Search error:', error));
        }, 300);
    });
}

function displaySearchResults(results) {
    const resultsContainer = document.querySelector('.search-results');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found</p>';
        return;
    }
    
    const html = results.map(item => `
        <div class="search-result-item">
            <img src="${item.image_url}" alt="${item.name}">
            <div>
                <h5>${item.name}</h5>
                <p>${item.category}</p>
                <span>$${item.price}</span>
            </div>
            <a href="/menu/${item.id}/" class="btn btn-small">View</a>
        </div>
    `).join('');
    
    resultsContainer.innerHTML = html;
}

// ===========================
// FORM VALIDATION
// ===========================

function validateBookingForm(form) {
    const name = form.querySelector('[name="name"]').value.trim();
    const email = form.querySelector('[name="email"]').value.trim();
    const date = form.querySelector('[name="date"]').value;
    const time = form.querySelector('[name="time"]').value;
    const people = form.querySelector('[name="number_of_people"]').value;

    if (!name || !email || !date || !time || !people) {
        showNotification('Please fill in all required fields', 'error');
        return false;
    }

    if (!isValidEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return false;
    }

    if (people < 1 || people > 50) {
        showNotification('Number of people must be between 1 and 50', 'error');
        return false;
    }

    return true;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ===========================
// NOTIFICATIONS
// ===========================

function showNotification(message, type = 'info') {
    const notif = document.createElement('div');
    notif.className = `notification notification-${type}`;
    notif.textContent = message;
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background-color: ${type === 'error' ? '#f8d7da' : '#d4edda'};
        color: ${type === 'error' ? '#721c24' : '#155724'};
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// ===========================
// ALERT REMOVAL
// ===========================

function removeAlerts() {
    document.querySelectorAll('.btn-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.alert').remove();
        });
    });
}

// ===========================
// CATEGORY FILTER
// ===========================

const categorySelect = document.querySelector('#category');
if (categorySelect) {
    categorySelect.addEventListener('change', function() {
        this.closest('form').submit();
    });
}

// ===========================
// NUMBER INPUT SPINNER
// ===========================

document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('change', function() {
        if (this.value < parseInt(this.min)) {
            this.value = this.min;
        }
        if (this.value > parseInt(this.max)) {
            this.value = this.max;
        }
    });
});

// ===========================
// KEYBOARD SHORTCUTS
// ===========================

document.addEventListener('keydown', function(event) {
    // Press 'H' to go home
    if (event.key === 'h' || event.key === 'H') {
        if (!isInputFocused()) {
            window.location.href = '/';
        }
    }
    
    // Press 'M' to go to menu
    if (event.key === 'm' || event.key === 'M') {
        if (!isInputFocused()) {
            window.location.href = '/menu/';
        }
    }
    
    // Press 'B' to book table
    if (event.key === 'b' || event.key === 'B') {
        if (!isInputFocused()) {
            window.location.href = '/book-table/';
        }
    }
});

function isInputFocused() {
    const activeElement = document.activeElement;
    const tagName = activeElement.tagName.toLowerCase();
    return tagName === 'input' || tagName === 'textarea' || tagName === 'select';
}

// ===========================
// ANIMATIONS - CSS ADDITIONS
// ===========================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .nav-menu.active {
        max-height: 600px;
    }
    
    @media (max-width: 768px) {
        .nav-menu {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            flex-direction: column;
            background-color: #2c1810;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }
        
        .nav-item {
            padding: 15px 20px;
            border-bottom: 1px solid #443322;
        }
        
        .nav-link {
            display: block;
        }
    }
`;
document.head.appendChild(style);

// ===========================
// LOCAL STORAGE HELPERS
// ===========================

function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function getFromLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (error) {
        console.error('Error retrieving from localStorage:', error);
        return null;
    }
}

// ===========================
// LAZY LOAD IMAGES
// ===========================

function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

lazyLoadImages();

// ===========================
// FORM SUBMIT HANDLER
// ===========================

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (this.classList.contains('booking-form')) {
            // Add loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            
            // Re-enable after 2 seconds
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }, 2000);
        }
    });
});

// ===========================
// AUTH TABS
// ===========================

function showLogin() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('signup-form').style.display = 'none';
    document.querySelectorAll('.auth-tab')[0].classList.add('active');
    document.querySelectorAll('.auth-tab')[1].classList.remove('active');
}

function showSignup() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('signup-form').style.display = 'block';
    document.querySelectorAll('.auth-tab')[0].classList.remove('active');
    document.querySelectorAll('.auth-tab')[1].classList.add('active');
}

console.log('Cafe Management System - JavaScript loaded successfully');
