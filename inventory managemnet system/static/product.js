// ---------------------------
// Load Products
// ---------------------------

window.onload = function () {

    console.log("Product JS Loaded");

    if (document.getElementById("productTable")) {
        loadProducts();
    }

};

// ---------------------------
// Save Product
// ---------------------------

async function saveProduct() {

    let product = {
        product_id: document.getElementById("productID").value.trim(),
        product_name: document.getElementById("productName").value.trim(),
        price: document.getElementById("price").value,
        quantity: document.getElementById("quantity").value,
        category: "",
        supplier: ""
    };

    if (
        product.product_id == "" ||
        product.product_name == "" ||
        product.price == "" ||
        product.quantity == ""
    ) {
        alert("Please fill all fields");
        return;
    }

    let response = await fetch("/api/add_product", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(product)

    });

    let result = await response.json();

    alert(result.message);

    clearForm();

}

// ---------------------------
// Load Products
// ---------------------------

async function loadProducts() {

    let response = await fetch("/api/products");

    let products = await response.json();

    let table = document.getElementById("productTable");

    table.innerHTML = "";

    products.forEach(product => {

        let status =
            Number(product.quantity) <= 5
                ? "<span style='color:red;font-weight:bold'>Low Stock</span>"
                : "<span style='color:green;font-weight:bold'>In Stock</span>";

        table.innerHTML += `

<tr>

<td>${product.product_id}</td>

<td>${product.product_name}</td>

<td>₹${product.price}</td>

<td>${product.quantity}</td>

<td>₹${product.price * product.quantity}</td>

<td>${status}</td>

<td>

<button onclick="deleteProduct(${product.id})">

Delete

</button>

</td>

</tr>

`;

    });

}

// ---------------------------
// Delete Product
// ---------------------------

async function deleteProduct(id){

    if(!confirm("Delete Product?")) return;

    await fetch("/api/delete_product/"+id,{
        method:"DELETE"
    });

    loadProducts();

}

// ---------------------------
// Search
// ---------------------------

function searchProduct(){

let value=document.getElementById("search").value.toLowerCase();

let rows=document.querySelectorAll("#productTable tr");

rows.forEach(row=>{

row.style.display=row.innerText.toLowerCase().includes(value)
?"":"none";

});

}

// ---------------------------
// Clear Form
// ---------------------------

function clearForm(){

document.getElementById("productID").value="";
document.getElementById("productName").value="";
document.getElementById("price").value="";
document.getElementById("quantity").value="";

}