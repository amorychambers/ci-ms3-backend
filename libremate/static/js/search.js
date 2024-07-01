const search = document.getElementById("search");
const books = document.getElementsByClassName("card");

search.addEventListener("input", function (e) {
    let searchTerm = e.target.value.toLowerCase();
    for (let book of books) {
        let title = book.getElementsByClassName("card-title")[0];
        let author = book.getElementsByClassName("card-subtitle")[0];
        if (!title.innerText.toLowerCase().includes(searchTerm) && !author.innerText.toLowerCase().includes(searchTerm)) {
            book.classList.add("d-none")
        } else {
            book.classList.remove("d-none")
        }
    }
});