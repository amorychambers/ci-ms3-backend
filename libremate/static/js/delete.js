let confirmDelete = document.getElementById("confirmDelete");
let deleteButton = document.getElementById("deleteButton");

confirmDelete.addEventListener("click", function() {
    if (deleteButton.classList.contains("disabled")){
        deleteButton.classList.remove("disabled");
    } else {
        deleteButton.classList.add("disabled")
    }
});