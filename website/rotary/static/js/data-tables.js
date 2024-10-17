import $ from 'jquery';
import 'datatables.net-bm';
import 'datatables.net-bm/css/dataTables.bulma.css';

$(document).ready(function() {
    $('#beersTable').DataTable({
        pageLength: 50,
        lengthMenu: [ [50, 100, 500, -1], [50, 100, 500, "All"] ]
    });
    $('#shiftsTable').DataTable({
        pageLength: 50,
        lengthMenu: [ [50, 100, -1], [50, 100, "All"] ],
        order: [[0, 'desc']]
    });
});