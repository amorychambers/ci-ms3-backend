// Initialize Bootstrap popovers
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

let checkButton = document.getElementById("cover-check");
let userConfirmation = document.getElementById("user-confirmation");
let confirmButton = document.getElementById("confirm");
let rejectButton = document.getElementById("reject");
let input = document.getElementById("isbn");
let cover = document.getElementById("cover");

checkButton.addEventListener('click', checkCover);
confirmButton.addEventListener('click', confirmCover);
rejectButton.addEventListener('click', rejectCover);

function checkCover(event){
    event.preventDefault();
    event.stopPropagation();
    checkButton.classList.add("disabled")

    userConfirmation.classList.remove("d-none")

    cover.setAttribute("src", `https://covers.openlibrary.org/b/isbn/${input.value}-L.jpg`);

    userConfirmation.insertAdjacentElement('afterbegin', cover);
}

function confirmCover(event){
    event.preventDefault();
    event.stopPropagation();

    userConfirmation.classList.add("d-none");
    checkButton.remove();

    let message = document.createElement("p");
    message.classList.add("valid-feedback", "d-inline", "mx-3")
    message.innerHTML = "Confirmed! &check;"

    userConfirmation.insertAdjacentElement("beforebegin", message)
}

function rejectCover(event){
    event.preventDefault();
    event.stopPropagation();

    userConfirmation.classList.add("d-none");
    checkButton.classList.remove("disabled");

    input.value = 0;

}
