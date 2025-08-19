import { initializeTable } from './tableutils.js';

document.addEventListener('DOMContentLoaded', function () {
    initializeTable('unavailableBeersTable', 'searchInput', 'unavailablePagination', 25);
    initializeTable('onMenuBeersTable', 'searchInput', 'onMenuPagination', 25);
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
            // Then we move the row to other table 
            // For some reason there is no need to remove tableRow from old table
            onMenuBeersBody.prepend(tableRow);
            // Do DB stuff here
            const beerId = tableRow.id;
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
            unavailableBeersBody.prepend(tableRow);
            // Do DB stuff here
            const beerId = tableRow.id;
            const requestUrl = window.location.origin + button.getAttribute("data-url");
            //Ignore fetch response, just post a toggle
            fetch(requestUrl, {
                method: "POST"
            });
        }
    });
});

