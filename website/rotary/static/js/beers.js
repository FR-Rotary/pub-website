import $ from 'jquery';
import 'datatables.net-bm';

$(document).ready(function() {
    $('#beersTable').DataTable({
        pageLength: 50,
        lengthMenu: [ [50, 100, 500, -1], [50, 100, 500, "All"] ]
    });
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