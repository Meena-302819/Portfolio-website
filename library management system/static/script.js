// ==========================================
// Library Management System
// script.js
// ==========================================

// ----------------------------
// Page Load
// ----------------------------

window.onload = function () {

    if (document.getElementById("totalBooks"))
        loadDashboard();

    if (document.getElementById("bookTable"))
        loadBooks();

    if (document.getElementById("issuedTable"))
        loadIssuedBooks();

    if (document.getElementById("returnedTable"))
        loadReturnedBooks();

    if (document.getElementById("reportTable"))
        loadReports();

};

// ----------------------------
// Login
// ----------------------------

function login(){

    let username=document.getElementById("username").value.trim();
    let password=document.getElementById("password").value.trim();

    if(username=="admin" && password=="admin123"){

        window.location.href="/dashboard";

    }
    else{

        document.getElementById("message").innerHTML="Invalid Username or Password";

    }

}

// ----------------------------
// Logout
// ----------------------------

function logout(){

    if(confirm("Do you want to Logout?")){

        window.location.href="/";

    }

}

// ----------------------------
// Dashboard
// ----------------------------

async function loadDashboard(){

    let response=await fetch("/api/dashboard");

    let data=await response.json();

    document.getElementById("totalBooks").innerHTML=data.totalBooks;
    document.getElementById("totalQuantity").innerHTML=data.totalQuantity;
    document.getElementById("availableBooks").innerHTML=data.availableBooks;
    document.getElementById("issuedBooks").innerHTML=data.issuedBooks;

}
// ----------------------------
// Save Book
// ----------------------------

async function saveBook(){

    let book={

        book_id:document.getElementById("bookID").value.trim(),
        book_name:document.getElementById("bookName").value.trim(),
        author:document.getElementById("author").value.trim(),
        category:document.getElementById("category").value.trim(),
        quantity:document.getElementById("quantity").value

    };

    if(

        book.book_id=="" ||
        book.book_name=="" ||
        book.author=="" ||
        book.category=="" ||
        book.quantity==""

    ){

        alert("Please Fill All Fields");
        return;

    }

    let response=await fetch("/api/add_book",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(book)

    });

    let result=await response.json();

    alert(result.message);

    clearBookForm();

    loadDashboard();

}



// ----------------------------
// Clear Book Form
// ----------------------------

function clearBookForm(){

    document.getElementById("bookID").value="";
    document.getElementById("bookName").value="";
    document.getElementById("author").value="";
    document.getElementById("category").value="";
    document.getElementById("quantity").value="";

}



// ----------------------------
// Load Books
// ----------------------------

async function loadBooks(){

    let response=await fetch("/api/books");

    let books=await response.json();

    let table=document.getElementById("bookTable");

    table.innerHTML="";

    books.forEach(book=>{

        table.innerHTML+=`

        <tr>

        <td>${book.book_id}</td>

        <td>${book.book_name}</td>

        <td>${book.author}</td>

        <td>${book.category}</td>

        <td>${book.quantity}</td>

        <td>${book.available}</td>

        <td>

        <button class="edit-btn"
        onclick="editBook(${book.id})">

        Edit

        </button>

        <button class="delete-btn"
        onclick="deleteBook(${book.id})">

        Delete

        </button>

        </td>

        </tr>

        `;

    });

}



// ----------------------------
// Delete Book
// ----------------------------

async function deleteBook(id){

    if(!confirm("Delete this Book?")) return;

    await fetch("/api/delete_book/"+id,{

        method:"DELETE"

    });

    loadBooks();

    loadDashboard();

}



// ----------------------------
// Edit Book
// ----------------------------

async function editBook(id){

    let response=await fetch("/api/book/"+id);

    let book=await response.json();

    document.getElementById("bookID").value=book.book_id;
    document.getElementById("bookName").value=book.book_name;
    document.getElementById("author").value=book.author;
    document.getElementById("category").value=book.category;
    document.getElementById("quantity").value=book.quantity;

}
// ==========================================
// Part 3
// Search + Issue + Return
// ==========================================

// ----------------------------
// Search Book
// ----------------------------

async function searchBook(){

    let keyword = document.getElementById("search").value.trim();

    if(keyword==""){

        loadBooks();
        return;

    }

    let response = await fetch("/api/search/"+keyword);

    let books = await response.json();

    let table = document.getElementById("bookTable");

    table.innerHTML="";

    books.forEach(book=>{

        table.innerHTML+=`

        <tr>

        <td>${book.book_id}</td>

        <td>${book.book_name}</td>

        <td>${book.author}</td>

        <td>${book.category}</td>

        <td>${book.quantity}</td>

        <td>${book.available}</td>

        <td>

        <button class="edit-btn"
        onclick="editBook(${book.id})">

        Edit

        </button>

        <button class="delete-btn"
        onclick="deleteBook(${book.id})">

        Delete

        </button>

        </td>

        </tr>

        `;

    });

}



// ----------------------------
// Issue Book
// ----------------------------

async function issueBook(){

    let data={

        book_id:document.getElementById("bookID").value.trim(),
        student_name:document.getElementById("studentName").value.trim(),
        roll_no:document.getElementById("rollNo").value.trim()

    };

    if(

        data.book_id=="" ||
        data.student_name=="" ||
        data.roll_no==""

    ){

        alert("Please Fill All Fields");
        return;

    }

    let response=await fetch("/api/issue_book",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(data)

    });

    let result=await response.json();

    alert(result.message);

    document.getElementById("bookID").value="";
    document.getElementById("studentName").value="";
    document.getElementById("rollNo").value="";

    loadDashboard();

}



// ----------------------------
// Load Issue History
// ----------------------------

async function loadIssuedBooks(){

    let response=await fetch("/api/issued_books");

    let books=await response.json();

    let table=document.getElementById("issuedTable");

    table.innerHTML="";

    books.forEach(book=>{

        table.innerHTML+=`

        <tr>

        <td>${book.book_id}</td>

        <td>${book.book_name}</td>

        <td>${book.student_name}</td>

        <td>${book.roll_no}</td>

        <td>${book.issue_date}</td>

        </tr>

        `;

    });

}



// ----------------------------
// Return Book
// ----------------------------

async function returnBook(){

    let data={

        book_id:document.getElementById("bookID").value.trim(),
        roll_no:document.getElementById("rollNo").value.trim()

    };

    if(

        data.book_id=="" ||
        data.roll_no==""

    ){

        alert("Please Fill All Fields");
        return;

    }

    let response=await fetch("/api/return_book",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(data)

    });

    let result=await response.json();

    alert(result.message);

    document.getElementById("bookID").value="";
    document.getElementById("rollNo").value="";

    loadDashboard();

}
// ==========================================
// Part 4
// Returned Books + Reports + Helpers
// ==========================================

// ----------------------------
// Load Returned Books
// ----------------------------

async function loadReturnedBooks(){

    let response = await fetch("/api/returned_books");

    let books = await response.json();

    let table = document.getElementById("returnedTable");

    if(!table) return;

    table.innerHTML = "";

    books.forEach(book=>{

        table.innerHTML += `

        <tr>

        <td>${book.book_id}</td>

        <td>${book.book_name}</td>

        <td>${book.student_name}</td>

        <td>${book.roll_no}</td>

        <td>${book.issue_date}</td>

        <td>${book.return_date}</td>

        </tr>

        `;

    });

}



// ----------------------------
// Reports
// ----------------------------

async function loadReports(){

    let response = await fetch("/api/reports");

    let data = await response.json();

    if(document.getElementById("totalBooks"))
        document.getElementById("totalBooks").innerHTML = data.totalBooks;

    if(document.getElementById("totalQuantity"))
        document.getElementById("totalQuantity").innerHTML = data.totalQuantity;

    if(document.getElementById("availableBooks"))
        document.getElementById("availableBooks").innerHTML = data.availableBooks;

    if(document.getElementById("issuedBooks"))
        document.getElementById("issuedBooks").innerHTML = data.issuedBooks;

    let table = document.getElementById("reportTable");

    if(!table) return;

    table.innerHTML = "";

    data.books.forEach(book=>{

        table.innerHTML += `

        <tr>

        <td>${book.book_id}</td>

        <td>${book.book_name}</td>

        <td>${book.author}</td>

        <td>${book.category}</td>

        <td>${book.quantity}</td>

        <td>${book.available}</td>

        </tr>

        `;

    });

}



// ----------------------------
// Refresh Page
// ----------------------------

function refreshPage(){

    location.reload();

}



// ----------------------------
// Clear Search
// ----------------------------

function clearSearch(){

    let search=document.getElementById("search");

    if(search){

        search.value="";

        loadBooks();

    }

}



// ----------------------------
// Auto Refresh Dashboard
// ----------------------------

setInterval(function(){

    if(document.getElementById("totalBooks")){

        loadDashboard();

    }

},5000);



// ==========================================
// End of script.js
// ==========================================