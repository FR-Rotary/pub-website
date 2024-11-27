import { initializeTable } from './tableutils.js';

document.addEventListener('DOMContentLoaded', function () {
    initializeTable('beersTable', 'searchInput', 'pagination', 25);
    
    // Move this event listener setup inside DOMContentLoaded
    function setupToggleListeners() {
        const forms = document.querySelectorAll('.toggle-beer-form');
        forms.forEach(function (form) {
            const checkbox = form.querySelector('.chungus-checkbox');
            if (checkbox && !checkbox.hasListener) {
                checkbox.hasListener = true;
                checkbox.addEventListener('change', function () {
                    form.submit();
                });
            }
        });
    }
    
    // Initial setup
    setupToggleListeners();
    
    // Setup observer to handle dynamically loaded content
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                setupToggleListeners();
            }
        });
    });
    
    // Start observing the table body for changes
    const tbody = document.querySelector('#beersTable tbody');
    observer.observe(tbody, { childList: true, subtree: true });
});