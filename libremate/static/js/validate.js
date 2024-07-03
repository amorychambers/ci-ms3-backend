/**
 * Code snippet taken from Bootstrap 5 docs regarding custom form validation, bypassing the default browser validation.
 * This code validates the form to register a new user, and allows custom feedback to be displayed in case of incorrect input.
 * This module is loaded on all pages where the user can submit a form that requires input validation.
 * These are account.html, add_book.html, add_genre.html, edit_book.html, register.html and sign_in.html.
 */
(() => {
    'use strict'

    const forms = document.querySelectorAll('.needs-validation')

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()

// Code to confirm password matches custom password, customised from Diego Leme snippet linked in readme
const password = document.getElementById("new-password");
const confirm = document.getElementById("confirm");

function validatePassword() {
    if (password.value != confirm.value) {
        confirm.setCustomValidity("Passwords do not match");
    } else {
        confirm.setCustomValidity("");
    }
}
confirm.addEventListener("keyup", e => {
    validatePassword();
});
