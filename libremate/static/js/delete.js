/**
 * This short module is loaded on the page where the user can choose to delete their account.
 * It only enables the button that deletes the user's account and data from the database once they have checked a confirmation box.
 */
let confirmDelete = document.getElementById("confirmDelete");
let deleteButton = document.getElementById("deleteButton");

confirmDelete.addEventListener("click", function() {
    if (deleteButton.classList.contains("disabled")){
        deleteButton.classList.remove("disabled");
    } else {
        deleteButton.classList.add("disabled")
    }
});