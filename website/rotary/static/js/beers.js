import { initializeTable } from './tableutils.js';

document.addEventListener('DOMContentLoaded', function () {
    initializeTable('beersTable', 'searchInput', 'pagination', 25);
});

document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.toggle-beer-form');

    forms.forEach(function (form) {
      const checkbox = form.querySelector('.chungus-checkbox');
      checkbox.addEventListener('change', function () {
        form.submit();
      });
    });
  });
