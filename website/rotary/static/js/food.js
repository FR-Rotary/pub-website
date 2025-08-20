import { addRowToTable, removeRowFromTable, initializeTable } from './tableutils.js';

document.addEventListener('DOMContentLoaded', function() {
	const unavailableFoodsTableObj = initializeTable('unavailableFoodsTable', 'foodSearchInput', 'foodPaginationInput', 'unavailableFoodsPagination', 25);
	const onMenuFoodsTableObj = initializeTable('onMenuFoodsTable', 'foodSearchInput', 'foodPaginationInput', 'onMenuFoodsPagination', 25);
	const unavailableSnacksTableObj = initializeTable('unavailableSnacksTable', 'snackSearchInput', 'snackPaginationInput', 'unavailableSnacksPagination', 25);
	const onMenuSnacksTableObj = initializeTable('onMenuSnacksTable', 'snackSearchInput', 'snackPaginationInput', 'onMenuSnacksPagination', 25);
	// Move this event listener setup inside DOMContentLoaded
	const unavailableFoodsBody = document.getElementById("unavailableFoodsTableBody");
	const onMenuFoodsBody = document.getElementById("onMenuFoodsTableBody");
	const unavailableSnacksBody = document.getElementById("unavailableSnacksTableBody");
	const onMenuSnacksBody = document.getElementById("onMenuSnacksTableBody");
	unavailableFoodsBody.addEventListener("click", function(event) {
		if (event.target.matches(".arrow-right")) {
			// We found right arrow, time to move food to "On Menu"

			// First we change the button class/id to match target
			const tableRow = event.target.closest("tr");
			const button = event.target.closest("button");
			button.setAttribute("class", "button is-danger arrow-left ")
			button.children[0].setAttribute("class", "icon arrow-left")
			button.children[0].children[0].setAttribute("class", "fas fa-arrow-left arrow-left")
			// Then we move the row to other ta:ble 
			// For some reason there is no need to remove tableRow from old table
			addRowToTable(onMenuFoodsTableObj, tableRow)
			removeRowFromTable(unavailableFoodsTableObj, tableRow);
			// Do DB stuff here
			const requestUrl = window.location.origin + button.getAttribute("data-url");
			//Ignore fetch response, just post a toggle
			fetch(requestUrl, {
				method: "POST"
			});
		}
	});
	onMenuFoodsBody.addEventListener("click", function(event) {
		if (event.target.matches(".arrow-left")) {
			// We found left arrow, time to move food to "Unavailable"

			// First we change the button class/id to match target
			const tableRow = event.target.closest("tr");
			const button = event.target.closest("button");
			button.setAttribute("class", "arrow-right button is-success")
			button.children[0].setAttribute("class", "icon arrow-right")
			button.children[0].children[0].setAttribute("class", "fas fa-arrow-right arrow-right")
			// Then we move the row to other table 
			// For some reason there is no need to remove tableRow from old table
			addRowToTable(unavailableFoodsTableObj, tableRow)
			removeRowFromTable(onMenuFoodsTableObj, tableRow);

			//unavailableFoodsBody.prepend(tableRow);
			// Do DB stuff here
			const requestUrl = window.location.origin + button.getAttribute("data-url");
			//Ignore fetch response, just post a toggle
			fetch(requestUrl, {
				method: "POST"
			});
		}
	});
	unavailableSnacksBody.addEventListener("click", function(event) {
		if (event.target.matches(".arrow-right")) {
			// We found right arrow, time to move snack to "On Menu"

			// First we change the button class/id to match target
			const tableRow = event.target.closest("tr");
			const button = event.target.closest("button");
			button.setAttribute("class", "button is-danger arrow-left ")
			button.children[0].setAttribute("class", "icon arrow-left")
			button.children[0].children[0].setAttribute("class", "fas fa-arrow-left arrow-left")
			// Then we move the row to other ta:ble 
			// For some reason there is no need to remove tableRow from old table
			addRowToTable(onMenuSnacksTableObj, tableRow)
			removeRowFromTable(unavailableSnacksTableObj, tableRow);
			// Do DB stuff here
			const requestUrl = window.location.origin + button.getAttribute("data-url");
			//Ignore fetch response, just post a toggle
			fetch(requestUrl, {
				method: "POST"
			});
		}
	});
	onMenuSnacksBody.addEventListener("click", function(event) {
		if (event.target.matches(".arrow-left")) {
			// We found left arrow, time to move snack to "Unavailable"

			// First we change the button class/id to match target
			const tableRow = event.target.closest("tr");
			const button = event.target.closest("button");
			button.setAttribute("class", "arrow-right button is-success")
			button.children[0].setAttribute("class", "icon arrow-right")
			button.children[0].children[0].setAttribute("class", "fas fa-arrow-right arrow-right")
			// Then we move the row to other table 
			// For some reason there is no need to remove tableRow from old table
			addRowToTable(unavailableSnacksTableObj, tableRow)
			removeRowFromTable(onMenuSnacksTableObj, tableRow);

			//unavailableSnacksBody.prepend(tableRow);
			// Do DB stuff here
			const requestUrl = window.location.origin + button.getAttribute("data-url");
			//Ignore fetch response, just post a toggle
			fetch(requestUrl, {
				method: "POST"
			});
		}
	});
});

