// Load Products
let products = JSON.parse(localStorage.getItem("products")) || [];
let editIndex = -1;

// ---------- Dashboard ----------
function updateDashboard() {

    let totalProducts = products.length;
    let totalStock = 0;
    let lowStock = 0;

    products.forEach((p) => {
        let qty = Number(p.qty || p.quantity || 0);
        totalStock += qty;

        if (qty <= 5) {
            lowStock++;
        }
    });

    if (document.getElementById("totalProducts"))
        document.getElementById("totalProducts").innerHTML = totalProducts;

    if (document.getElementById("totalStock"))
        document.getElementById("totalStock").innerHTML = totalStock;

    if (document.getElementById("lowStock"))
        document.getElementById("lowStock").innerHTML = lowStock;
}

// ---------- Products Table ----------
function displayProducts() {

    updateDashboard();

    let table = document.getElementById("tableData");

    if (!table) return;

    table.innerHTML = "";

    products.forEach((p, index) => {

        let qty = Number(p.qty || p.quantity || 0);

        let status =
            qty <= 5
                ? "<span style='color:red;font-weight:bold'>Low Stock</span>"
                : "<span style='color:green;font-weight:bold'>In Stock</span>";

        table.innerHTML += `
        <tr>
            <td>${p.id}</td>
            <td>${p.name}</td>
            <td>₹${p.price}</td>
            <td>${qty}</td>
            <td>₹${p.price * qty}</td>
            <td>${status}</td>
            <td>
                <button class="edit" onclick="editProduct(${index})">Edit</button>
                <button class="delete" onclick="deleteProduct(${index})">Delete</button>
            </td>
        </tr>
        `;
    });

}

// ---------- Add Product ----------
function addProduct() {

    let name = document.getElementById("productName").value.trim();
    let id = document.getElementById("productID").value.trim();
    let price = parseFloat(document.getElementById("price").value);
    let qty = parseInt(document.getElementById("quantity").value);

    if (!name || !id || isNaN(price) || isNaN(qty)) {
        alert("Please fill all fields.");
        return;
    }

    let product = {
        id,
        name,
        price,
        qty
    };

    if (editIndex === -1) {
        products.push(product);
    } else {
        products[editIndex] = product;
        editIndex = -1;
    }

    saveData();
    clearFields();
    displayProducts();

}

// ---------- Edit ----------
function editProduct(index) {

    let p = products[index];

    document.getElementById("productName").value = p.name;
    document.getElementById("productID").value = p.id;
    document.getElementById("price").value = p.price;
    document.getElementById("quantity").value = p.qty;

    editIndex = index;

}

// ---------- Delete ----------
function deleteProduct(index) {

    if (confirm("Delete this product?")) {

        products.splice(index, 1);

        saveData();

        displayProducts();

    }

}

// ---------- Search ----------
function searchProduct() {

    let search = document.getElementById("search");

    if (!search) return;

    let value = search.value.toLowerCase();

    document.querySelectorAll("#tableData tr").forEach(row => {

        row.style.display =
            row.innerText.toLowerCase().includes(value)
                ? ""
                : "none";

    });

}

// ---------- Save ----------
function saveData() {

    localStorage.setItem("products", JSON.stringify(products));

}

// ---------- Clear ----------
function clearFields() {

    if(document.getElementById("productName"))
        document.getElementById("productName").value="";

    if(document.getElementById("productID"))
        document.getElementById("productID").value="";

    if(document.getElementById("price"))
        document.getElementById("price").value="";

    if(document.getElementById("quantity"))
        document.getElementById("quantity").value="";

}

// ---------- Load ----------
window.onload = function(){

    displayProducts();

};
// -----------------------------
// Dashboard & Reports
// -----------------------------

window.addEventListener("load", () => {

    loadDashboard();

});

async function loadDashboard(){

    let response = await fetch("/api/dashboard");

    let data = await response.json();

    if(document.getElementById("totalProducts"))
        document.getElementById("totalProducts").innerHTML=data.totalProducts;

    if(document.getElementById("totalStock"))
        document.getElementById("totalStock").innerHTML=data.totalStock;

    if(document.getElementById("lowStock"))
        document.getElementById("lowStock").innerHTML=data.lowStock;

    if(document.getElementById("inventoryValue"))
        document.getElementById("inventoryValue").innerHTML="₹"+data.inventoryValue;

}