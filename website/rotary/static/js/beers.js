import $ from 'jquery';
import 'datatables.net-bm';

$(document).ready(function() {
    $('#beersTable').DataTable({
        pageLength: 50,
        lengthMenu: [ [50, 100, 500, -1], [50, 100, 500, "All"] ]
    });
});
