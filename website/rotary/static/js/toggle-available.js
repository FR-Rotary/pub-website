document.addEventListener('DOMContentLoaded', function () {
    const toggleForms = document.querySelectorAll('.toggle-availability-form');

    toggleForms.forEach(form => {
        const checkbox = form.querySelector('.chungus-checkbox');
        checkbox.addEventListener('change', function () {
            form.submit();
        });
    });
});