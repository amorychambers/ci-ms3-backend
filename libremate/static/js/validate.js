// Validate the form to register a new user
// Code to use custom validation taken from Bootstrap 5 docs
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
