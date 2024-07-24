/**
 * This module is loaded on the register.html page and ensures that the password entered in the New Password and Confirm Password boxes are the same
 */
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