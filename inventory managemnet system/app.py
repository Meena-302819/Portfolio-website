from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Create Database Tables
# -----------------------------
def init_db():

    conn = get_db()
    cursor = conn.cursor()

    # Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT,
        product_name TEXT,
        category TEXT,
        supplier TEXT,
        quantity INTEGER,
        price REAL
    )
    """)

    # Categories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE
    )
    """)

    # Suppliers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# Page Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/add-product")
def add_product():
    return render_template("add-product.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/suppliers")
def suppliers():
    return render_template("suppliers.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")
# -----------------------------
# API : Add Product
# -----------------------------
@app.route("/api/add_product", methods=["POST"])
def api_add_product():

    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products
    (product_id, product_name, category, supplier, quantity, price)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["product_id"],
        data["product_name"],
        data.get("category", ""),
        data.get("supplier", ""),
        int(data["quantity"]),
        float(data["price"])
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Product Added Successfully"
    })


# -----------------------------
# API : Get Products
# -----------------------------
@app.route("/api/products", methods=["GET"])
def api_products():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# -----------------------------
# API : Delete Product
# -----------------------------
@app.route("/api/delete_product/<int:id>", methods=["DELETE"])
def delete_product(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Product Deleted Successfully"
    })


# -----------------------------
# API : Dashboard
# -----------------------------
@app.route("/api/dashboard", methods=["GET"])
def dashboard_api():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(SUM(quantity),0) FROM products")
    total_stock = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE quantity<=5")
    low_stock = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(SUM(price*quantity),0) FROM products")
    inventory_value = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "totalProducts": total_products,
        "totalStock": total_stock,
        "lowStock": low_stock,
        "inventoryValue": inventory_value
    })
# -----------------------------
# API : Add Category
# -----------------------------
@app.route("/api/add_category", methods=["POST"])
def add_category():

    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO categories(category_name) VALUES(?)",
        (data["category_name"],)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Category Added Successfully"
    })


# -----------------------------
# API : Get Categories
# -----------------------------
@app.route("/api/categories", methods=["GET"])
def get_categories():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categories")

    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# -----------------------------
# API : Delete Category
# -----------------------------
@app.route("/api/delete_category/<int:id>", methods=["DELETE"])
def delete_category(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM categories WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Category Deleted Successfully"
    })


# -----------------------------
# API : Add Supplier
# -----------------------------
@app.route("/api/add_supplier", methods=["POST"])
def add_supplier():

    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO suppliers
    (supplier_name, phone)
    VALUES (?, ?)
    """, (
        data["supplier_name"],
        data["phone"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Supplier Added Successfully"
    })


# -----------------------------
# API : Get Suppliers
# -----------------------------
@app.route("/api/suppliers", methods=["GET"])
def get_suppliers():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM suppliers")

    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# -----------------------------
# API : Delete Supplier
# -----------------------------
@app.route("/api/delete_supplier/<int:id>", methods=["DELETE"])
def delete_supplier(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM suppliers WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Supplier Deleted Successfully"
    })
# -----------------------------
# API : Reports
# -----------------------------
@app.route("/api/reports", methods=["GET"])
def reports_api():

    conn = get_db()
    cursor = conn.cursor()

    # All Products
    cursor.execute("SELECT * FROM products")
    products = [dict(row) for row in cursor.fetchall()]

    # Total Products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    # Total Stock
    cursor.execute("SELECT IFNULL(SUM(quantity),0) FROM products")
    total_stock = cursor.fetchone()[0]

    # Inventory Value
    cursor.execute("SELECT IFNULL(SUM(price * quantity),0) FROM products")
    inventory_value = cursor.fetchone()[0]

    # Low Stock
    cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= 5")
    low_stock = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "products": products,
        "totalProducts": total_products,
        "totalStock": total_stock,
        "inventoryValue": inventory_value,
        "lowStock": low_stock
    })


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5003)