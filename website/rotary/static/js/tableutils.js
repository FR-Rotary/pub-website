export function initializeTable(tableId, searchInputId, paginationInputId, paginationId, rowsPerPage = 25) {
    const tbody = document.getElementById(tableId).querySelector('tbody');
    const tableObj = {
        table: document.getElementById(tableId),
        tableBody: tbody,
        searchInput: document.getElementById(searchInputId),
        paginationInput: document.getElementById(paginationInputId),
        pagination: document.getElementById(paginationId),
        rowsPerPage: rowsPerPage,
        currentPage: 1,
        rows: Array.from(tbody.querySelectorAll('tr')),
    }
    tableObj.searchInput.addEventListener('input', () => renderTable(tableObj));
    tableObj.paginationInput.addEventListener('change', () => changeRowsPerPage(tableObj));

    // Initial render
    renderTable(tableObj);
    return tableObj;
}

export function renderTable(tableObj) {
    // Remove all entries
    tableObj.tableBody.innerHTML = '';
    // Find relevant entries
    const filteredRows = filterTable(tableObj)
    // Move to valid page if outside range
    const totalPages = Math.ceil(filteredRows.length / tableObj.rowsPerPage);
    if (tableObj.currentPage > totalPages && totalPages > 0) {
        tableObj.currentPage = totalPages
    }
    // Do pagination logic
    const start = (tableObj.currentPage - 1) * tableObj.rowsPerPage;
    const end = start + tableObj.rowsPerPage;
    filteredRows.slice(start, end).forEach(row => tableObj.tableBody.appendChild(row));
    // Display all pagination HTML
    renderPagination(tableObj, filteredRows.length);
};

export function addRowToTable(tableObj, row) {
    tableObj.rows.unshift(row)
    renderTable(tableObj)
}

export function removeRowFromTable(tableObj, row) {
    const index = tableObj.rows.indexOf(row);
    if (index > -1) {
        tableObj.rows.splice(index, 1)
    }
    renderTable(tableObj)
}

function createPageLink(tableObj, page, isCurrent = false) {
    const pageLink = document.createElement('a');
    pageLink.className = 'pagination-link';
    pageLink.textContent = page;
    pageLink.href = '#';
    if (isCurrent) {
        pageLink.classList.add('is-current');
        pageLink.setAttribute('aria-current', 'page');
    }
    pageLink.addEventListener('click', (e) => {
        e.preventDefault();
        tableObj.currentPage = page;
        renderTable(tableObj);
    });
    return pageLink;
};

function renderPagination(tableObj, nrOfRows) {
    const totalPages = Math.ceil(nrOfRows / tableObj.rowsPerPage);
    const paginationList = tableObj.pagination.querySelector('.pagination-list');
    const prevButton = tableObj.pagination.querySelector('.pagination-previous');
    const nextButton = tableObj.pagination.querySelector('.pagination-next');

    paginationList.innerHTML = '';
    prevButton.classList.toggle('is-disabled', tableObj.currentPage === 1);
    nextButton.classList.toggle('is-disabled', tableObj.currentPage === totalPages);

    prevButton.onclick = (e) => {
        e.preventDefault();
        if (tableObj.currentPage > 1) {
            tableObj.currentPage--;
            renderTable(tableObj);
        }
    };

    nextButton.onclick = (e) => {
        e.preventDefault();
        if (tableObj.currentPage < totalPages) {
            tableObj.currentPage++;
            renderTable(tableObj);
        }
    };

    if (totalPages <= 1) return;

    paginationList.appendChild(createPageLink(tableObj, 1, tableObj.currentPage === 1));
    if (tableObj.currentPage > 3) paginationList.appendChild(document.createElement('span')).className = 'pagination-ellipsis';

    for (let i = Math.max(2, tableObj.currentPage - 1); i <= Math.min(totalPages - 1, tableObj.currentPage + 1); i++) {
        paginationList.appendChild(createPageLink(tableObj, i, tableObj.currentPage === i));
    }

    if (tableObj.currentPage < totalPages - 2) paginationList.appendChild(document.createElement('span')).className = 'pagination-ellipsis';
    paginationList.appendChild(createPageLink(tableObj, totalPages, tableObj.currentPage === totalPages));
};

function filterTable(tableObj) {
    const query = tableObj.searchInput.value.toLowerCase();
    const filteredRows = tableObj.rows.filter(row => {
        return Array.from(row.cells).some(cell => {
            return cell.textContent.toLowerCase().includes(query);
        });
    });
    return filteredRows;
};

function changeRowsPerPage(tableObj) {
    const query = tableObj.paginationInput.value;
    tableObj.rowsPerPage = parseInt(query);
    renderTable(tableObj);
}
