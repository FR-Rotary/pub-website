import { initializeTable } from './tableutils.js';

document.addEventListener('DOMContentLoaded', function () {
    initializeTable('shiftsTable', 'searchInput', 'pagination', 25);
});

document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('workers-container');
    const addWorkerBtn = document.getElementById('add-worker');
    const removeWorkerBtn = document.getElementById('remove-worker');
    const toggleAllWorkersCheckbox = document.getElementById('toggle-all-workers');

    function addWorker() {
        const firstChild = container.children[0];
        if (firstChild) {
            const newSelect = firstChild.cloneNode(true);
            const selectElement = newSelect.querySelector('select');
            if (selectElement) {
                selectElement.value = selectElement.options[0].value;
            }
            container.appendChild(newSelect);
        }
    }

    function removeWorker() {
        if (container.children.length > 1) {
            container.removeChild(container.lastElementChild);
        } else {
            alert('At least one worker must be selected.');
        }
    }

    function updateWorkerSelectOptions() {
        const workersToUse = toggleAllWorkersCheckbox.checked ? allWorkers : activeWorkers;
        const workerSelects = container.querySelectorAll('.worker-select select[name="workerid[]"]');

        workerSelects.forEach(function (selectElement) {
            selectElement.innerHTML = ''; // Clear existing options

            // Add a default disabled option
            const defaultOption = document.createElement('option');
            defaultOption.value = "-1";
            defaultOption.disabled = true;
            defaultOption.selected = true;
            defaultOption.textContent = "Select Worker";
            selectElement.appendChild(defaultOption);

            // Populate with new options
            workersToUse.forEach(function (worker) {
                const option = document.createElement('option');
                option.value = worker.id;
                option.textContent = worker.display_name;
                selectElement.appendChild(option);
            });
        });
    }

    function initializeEventListeners() {
        addWorkerBtn.addEventListener('click', addWorker);
        removeWorkerBtn.addEventListener('click', removeWorker);
        toggleAllWorkersCheckbox.addEventListener('change', updateWorkerSelectOptions);
    }

    initializeEventListeners();
    updateWorkerSelectOptions();
});