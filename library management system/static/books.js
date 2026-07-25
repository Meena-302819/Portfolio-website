document.getElementById("bookForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let bookId = document.getElementById("bookId").value;
    let bookName = document.getElementById("bookName").value;
    let author = document.getElementById("author").value;
    let category = document.getElementById("category").value;
    let quantity = document.getElementById("quantity").value;

    let book = {
        bookId: bookId,
        bookName: bookName,
        author: author,
        category: category,
        quantity: quantity
    };

    let books = JSON.parse(localStorage.getItem("books")) || [];

    books.push(book);

    localStorage.setItem("books", JSON.stringify(books));

    document.getElementById("message").style.color = "green";
    document.getElementById("message").innerHTML = "Book Added Successfully!";

    document.getElementById("bookForm").reset();
});