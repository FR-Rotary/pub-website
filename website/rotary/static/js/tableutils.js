export function initializeTable(tableId, searchInputId, paginationId, rowsPerPage = 25) {
    const table = document.getElementById(tableId);
    const tbody = table.querySelector('tbody');
    const searchInput = document.getElementById(searchInputId);
    const pagination = document.getElementById(paginationId);
    let currentPage = 1;
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const createPageLink = (page, isCurrent = false) => {
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
            currentPage = page;
            filterTable();
        });
        return pageLink;
    };

    const renderTable = (filteredRows) => {
        tbody.innerHTML = '';
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        filteredRows.slice(start, end).forEach(row => tbody.appendChild(row));
        renderPagination(filteredRows.length);
    };

    const renderPagination = (totalRows) => {
        const totalPages = Math.ceil(totalRows / rowsPerPage);
        const paginationList = pagination.querySelector('.pagination-list');
        const prevButton = pagination.querySelector('.pagination-previous');
        const nextButton = pagination.querySelector('.pagination-next');

        paginationList.innerHTML = '';
        prevButton.classList.toggle('is-disabled', currentPage === 1);
        nextButton.classList.toggle('is-disabled', currentPage === totalPages);

        prevButton.onclick = (e) => {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                filterTable();
            }
        };

        nextButton.onclick = (e) => {
            e.preventDefault();
            if (currentPage < totalPages) {
                currentPage++;
                filterTable();
            }
        };

        if (totalPages <= 1) return;

        paginationList.appendChild(createPageLink(1, currentPage === 1));
        if (currentPage > 3) paginationList.appendChild(document.createElement('span')).className = 'pagination-ellipsis';

        for (let i = Math.max(2, currentPage - 1); i <= Math.min(totalPages - 1, currentPage + 1); i++) {
            paginationList.appendChild(createPageLink(i, currentPage === i));
        }

        if (currentPage < totalPages - 2) paginationList.appendChild(document.createElement('span')).className = 'pagination-ellipsis';
        paginationList.appendChild(createPageLink(totalPages, currentPage === totalPages));
    };

    const filterTable = () => {
        const query = searchInput.value.toLowerCase();
        const filteredRows = rows.filter(row => {
            return Array.from(row.cells).some(cell => {
                return cell.textContent.toLowerCase().includes(query);
            });
        });

        renderTable(filteredRows);
    };

    searchInput.addEventListener('input', filterTable);

    // Initial render
    renderTable(rows);
}