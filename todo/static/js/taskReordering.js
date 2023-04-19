var taskList = document.getElementById("task-list");
var reorderForm = document.getElementById("task-reorder-form");
var positionInput = document.getElementById("task-position-input");

let sortable = Sortable.create(taskList, {
    handle: '.handle',
    ghostClass: 'dropArea',
    chosenClass: 'selectedTask',

});

function reordering() {
    const rows = document.getElementsByClassName("task-wrapper");
    let pos = [];
    for (let row of rows) {
        pos.push(row.dataset.position);
    }

    positionInput.value = pos.join(',');
    reorderForm.submit();
}

document.ondrop = reordering;