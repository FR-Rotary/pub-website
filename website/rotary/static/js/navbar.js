document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
  
    // Function to apply the theme
    function applyTheme(theme) {
      body.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme); // Save theme preference
      themeToggle.checked = theme === 'light'; // Set checkbox state based on theme
    }
  
    // Check for saved theme preference and apply it
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      applyTheme(savedTheme);
    }
  
    themeToggle.addEventListener('change', () => {
      const newTheme = themeToggle.checked ? 'light' : 'dark';
      applyTheme(newTheme);
    });

  // Navbar Burger Toggle
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  if ($navbarBurgers.length > 0) {
    $navbarBurgers.forEach(el => {
      el.addEventListener('click', () => {
        const target = el.dataset.target;
        const $target = document.getElementById(target);
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
      });
    });
  }

  // Internal Dropdown Toggle
  const internalDropdown = document.getElementById('internal-dropdown');
  if (internalDropdown) {
    const internalLink = internalDropdown.querySelector('.navbar-link');
    internalLink.addEventListener('click', () => {
      internalDropdown.classList.toggle('is-active');
    });
  }

  function setCurrentYear() {
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
      yearElement.textContent = new Date().getFullYear();
    }
  }
  setCurrentYear();

});