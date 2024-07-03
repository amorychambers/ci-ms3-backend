/**
 * This file contains the functions related to the feature that lets users search for a cover image for their books by the ISBN.
 * It accesses data through the Open Library Covers API and gives the user the opportunity to confirm or reject the cover.
 */
let checkButton = document.getElementById("cover-check");
let userConfirmation = document.getElementById("user-confirmation");
let confirmButton = document.getElementById("confirm");
let rejectButton = document.getElementById("reject");
let input = document.getElementById("isbn");
let cover = document.getElementById("cover");

checkButton.addEventListener('click', checkCover);
confirmButton.addEventListener('click', confirmCover);
rejectButton.addEventListener('click', rejectCover);

/**
 * Takes the ISBN value input by the user and inserts it into the API link.
 * Displays the retrived cover image on the page and disables the button that calls the API until user confirms or rejects cover.
 */
function checkCover(event){
    event.preventDefault();
    event.stopPropagation();
    checkButton.classList.add("disabled");

    userConfirmation.classList.remove("d-none");

    cover.setAttribute("src", `https://covers.openlibrary.org/b/isbn/${input.value}-L.jpg`);

    userConfirmation.insertAdjacentElement('afterbegin', cover);
}

/**
 * Adds a confirmation message to show cover has been accepted after selecting Confirm button.
 * Preserves the ISBN input to be saved in the database, but allows user to search and try again. 
 */
function confirmCover(event){
    event.preventDefault();
    event.stopPropagation();

    userConfirmation.classList.add("d-none");
    checkButton.remove();

    let message = document.createElement("p");
    message.classList.add("valid-feedback", "d-inline", "mx-3");
    message.innerHTML = "Confirmed! &check;";

    userConfirmation.insertAdjacentElement("beforebegin", message);
}

/**
 * Resets the value of the ISBN input box to 0, which can be saved in the database to indicate no cover image retrieved and to use standardised site cover.
 * Re-enables button that calls API so user can search again.
 */
function rejectCover(event){
    event.preventDefault();
    event.stopPropagation();

    userConfirmation.classList.add("d-none");
    checkButton.classList.remove("disabled");

    input.value = 0;

}