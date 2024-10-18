document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const navbarBurgers = Array.from(document.querySelectorAll('.navbar-burger'));
    const internalDropdown = document.getElementById('internal-dropdown');
    const yearElement = document.getElementById('current-year');

    function applyTheme(theme) {
        body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        themeToggle.checked = theme === 'light';
    }

    function initializeTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            applyTheme(savedTheme);
        }
    }

    function setupThemeToggle() {
        themeToggle.addEventListener('change', () => {
            const newTheme = themeToggle.checked ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }

    function initializeNavbarBurgerToggle() {
        if (navbarBurgers.length > 0) {
            navbarBurgers.forEach(el => {
                el.addEventListener('click', () => {
                    const target = el.dataset.target;
                    const targetElement = document.getElementById(target);
                    el.classList.toggle('is-active');
                    targetElement.classList.toggle('is-active');
                });
            });
        }
    }

    function initializeInternalDropdownToggle() {
        if (internalDropdown) {
            const internalLink = internalDropdown.querySelector('.navbar-link');
            internalLink.addEventListener('click', () => {
                internalDropdown.classList.toggle('is-active');
            });
        }
    }

    function setCurrentYear() {
        if (yearElement) {
            yearElement.textContent = new Date().getFullYear();
        }
    }

    initializeTheme();
    setupThemeToggle();
    initializeNavbarBurgerToggle();
    initializeInternalDropdownToggle();
    setCurrentYear();
});