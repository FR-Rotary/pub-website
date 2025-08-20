import { addRowToTable, removeRowFromTable, initializeTable } from './tableutils.js';

document.addEventListener('DOMContentLoaded', function() {
    const unavailableTableObj = initializeTable('unavailableBeersTable', 'searchInput', 'paginationInput', 'unavailablePagination', 25);
    const onMenuTableObj = initializeTable('onMenuBeersTable', 'searchInput', 'paginationInput', 'onMenuPagination', 25);
    // Move this event listener setup inside DOMContentLoaded
    const unavailableBeersBody = document.getElementById("unavailableBeersTableBody");
    const onMenuBeersBody = document.getElementById("onMenuBeersTableBody");
    unavailableBeersBody.addEventListener("click", function(event) {
        if (event.target.matches(".arrow-right")) {
            // We found right arrow, time to move beer to "On Menu"

            // First we change the button class/id to match target
            const tableRow = event.target.closest("tr");
            const button = event.target.closest("button");
            button.setAttribute("class", "button is-danger arrow-left ")
            button.children[0].setAttribute("class", "icon arrow-left")
            button.children[0].children[0].setAttribute("class", "fas fa-arrow-left arrow-left")
            // Then we move the row to other ta:ble 
            // For some reason there is no need to remove tableRow from old table
            addRowToTable(onMenuTableObj, tableRow)
            removeRowFromTable(unavailableTableObj, tableRow);
            // Do DB stuff here
            const requestUrl = window.location.origin + button.getAttribute("data-url");
            //Ignore fetch response, just post a toggle
            fetch(requestUrl, {
                method: "POST"
            });
        }
    });
    onMenuBeersBody.addEventListener("click", function(event) {
        if (event.target.matches(".arrow-left")) {
            // We found left arrow, time to move beer to "Unavailable"

            // First we change the button class/id to match target
            const tableRow = event.target.closest("tr");
            const button = event.target.closest("button");
            button.setAttribute("class", "arrow-right button is-success")
            button.children[0].setAttribute("class", "icon arrow-right")
            button.children[0].children[0].setAttribute("class", "fas fa-arrow-right arrow-right")
            // Then we move the row to other table 
            // For some reason there is no need to remove tableRow from old table
            addRowToTable(unavailableTableObj, tableRow)
            removeRowFromTable(onMenuTableObj, tableRow);

            //unavailableBeersBody.prepend(tableRow);
            // Do DB stuff here
            const requestUrl = window.location.origin + button.getAttribute("data-url");
            //Ignore fetch response, just post a toggle
            fetch(requestUrl, {
                method: "POST"
            });
        }
    });
});

