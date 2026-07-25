from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Create Database
# -----------------------------
def init_db():

    conn = get_db()
    cur = conn.cursor()

    # Books Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id TEXT UNIQUE,
        book_name TEXT,
        author TEXT,
        category TEXT,
        quantity INTEGER,
        available INTEGER
    )
    """)

    # Issued Books
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issued_books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id TEXT,
        book_name TEXT,
        student_name TEXT,
        roll_no TEXT,
        issue_date TEXT
    )
    """)

    # Returned Books
    cur.execute("""
    CREATE TABLE IF NOT EXISTS returned_books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id TEXT,
        book_name TEXT,
        student_name TEXT,
        roll_no TEXT,
        issue_date TEXT,
        return_date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Pages
# -----------------------------

@app.route("/")
def login():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/books")
def books():
    return render_template("books.html")


@app.route("/addbook")
def addbook():
    return render_template("addbook.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/issue")
def issue():
    return render_template("issue.html")


@app.route("/return")
def return_book():
    return render_template("return.html")


@app.route("/issuedbooks")
def issuedbooks():
    return render_template("issuedbooks.html")


@app.route("/returnedbooks")
def returnedbooks():
    return render_template("returnedbooks.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")
# -----------------------------
# API : Add Book
# -----------------------------
@app.route("/api/add_book", methods=["POST"])
def add_book():

    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO books
    (book_id, book_name, author, category, quantity, available)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (

        data["book_id"],
        data["book_name"],
        data["author"],
        data["category"],
        int(data["quantity"]),
        int(data["quantity"])

    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"success",
        "message":"Book Added Successfully"
    })


# -----------------------------
# API : Get Books
# -----------------------------
@app.route("/api/books", methods=["GET"])
def get_books():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM books ORDER BY id DESC")

    books = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(books)


# -----------------------------
# API : Delete Book
# -----------------------------
@app.route("/api/delete_book/<int:id>", methods=["DELETE"])
def delete_book(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM books WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"success",
        "message":"Book Deleted Successfully"
    })


# -----------------------------
# API : Search Book
# -----------------------------
@app.route("/api/search/<keyword>")
def search_book(keyword):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM books

    WHERE

    book_name LIKE ?

    OR

    author LIKE ?

    OR

    category LIKE ?

    OR

    book_id LIKE ?

    """,

    (

    f"%{keyword}%",
    f"%{keyword}%",
    f"%{keyword}%",
    f"%{keyword}%"

    ))

    books = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(books)
# -----------------------------
# API : Issue Book
# -----------------------------
@app.route("/api/issue_book", methods=["POST"])
def issue_book():

    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    # Check Book
    cur.execute(
        "SELECT * FROM books WHERE book_id=?",
        (data["book_id"],)
    )

    book = cur.fetchone()

    if not book:
        conn.close()
        return jsonify({
            "status":"error",
            "message":"Book Not Found"
        })

    if book["available"] <= 0:
        conn.close()
        return jsonify({
            "status":"error",
            "message":"Book Not Available"
        })

    issue_date = datetime.now().strftime("%d-%m-%Y")

    cur.execute("""
    INSERT INTO issued_books
    (book_id, book_name, student_name, roll_no, issue_date)
    VALUES (?, ?, ?, ?, ?)
    """, (

        book["book_id"],
        book["book_name"],
        data["student_name"],
        data["roll_no"],
        issue_date

    ))

    cur.execute(
        "UPDATE books SET available=available-1 WHERE book_id=?",
        (book["book_id"],)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status":"success",
        "message":"Book Issued Successfully"
    })


# -----------------------------
# API : Return Book
# -----------------------------
@app.route("/api/return_book", methods=["POST"])
def return_book_api():

    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM issued_books

    WHERE

    book_id=?

    AND

    roll_no=?

    """,

    (

        data["book_id"],
        data["roll_no"]

    ))

    issue = cur.fetchone()

    if not issue:

        conn.close()

        return jsonify({
            "status":"error",
            "message":"Issue Record Not Found"
        })

    return_date = datetime.now().strftime("%d-%m-%Y")

    cur.execute("""

    INSERT INTO returned_books

    (

    book_id,
    book_name,
    student_name,
    roll_no,
    issue_date,
    return_date

    )

    VALUES

    (?, ?, ?, ?, ?, ?)

    """,

    (

        issue["book_id"],
        issue["book_name"],
        issue["student_name"],
        issue["roll_no"],
        issue["issue_date"],
        return_date

    ))

    cur.execute(
        "DELETE FROM issued_books WHERE id=?",
        (issue["id"],)
    )

    cur.execute(
        "UPDATE books SET available=available+1 WHERE book_id=?",
        (issue["book_id"],)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status":"success",
        "message":"Book Returned Successfully"
    })


# -----------------------------
# API : Issued Books
# -----------------------------
@app.route("/api/issued_books")
def issued_books():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM issued_books ORDER BY id DESC")

    books = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(books)


# -----------------------------
# API : Returned Books
# -----------------------------
@app.route("/api/returned_books")
def returned_books():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM returned_books ORDER BY id DESC")

    books = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(books)
# -----------------------------
# API : Get Single Book
# -----------------------------
@app.route("/api/book/<int:id>", methods=["GET"])
def get_single_book(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    )

    book = cur.fetchone()

    conn.close()

    if book:
        return jsonify(dict(book))

    return jsonify({
        "status":"error",
        "message":"Book Not Found"
    })


# -----------------------------
# API : Update Book
# -----------------------------
@app.route("/api/update_book/<int:id>", methods=["PUT"])
def update_book(id):

    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT available FROM books WHERE id=?",
        (id,)
    )

    old = cur.fetchone()

    if not old:
        conn.close()
        return jsonify({
            "status":"error",
            "message":"Book Not Found"
        })

    new_qty = int(data["quantity"])

    if old["available"] > new_qty:
        available = new_qty
    else:
        available = old["available"]

    cur.execute("""

    UPDATE books

    SET

    book_id=?,
    book_name=?,
    author=?,
    category=?,
    quantity=?,
    available=?

    WHERE id=?

    """,

    (

        data["book_id"],
        data["book_name"],
        data["author"],
        data["category"],
        new_qty,
        available,
        id

    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"success",
        "message":"Book Updated Successfully"
    })


# -----------------------------
# API : Dashboard
# -----------------------------
@app.route("/api/dashboard")
def dashboard_api():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM books")
    totalBooks = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(quantity),0) FROM books")
    totalQuantity = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(available),0) FROM books")
    availableBooks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issued_books")
    issuedBooks = cur.fetchone()[0]

    conn.close()

    return jsonify({

        "totalBooks": totalBooks,
        "totalQuantity": totalQuantity,
        "availableBooks": availableBooks,
        "issuedBooks": issuedBooks

    })


# -----------------------------
# API : Reports
# -----------------------------
@app.route("/api/reports")
def reports_api():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM books")

    books = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT COUNT(*) FROM books")
    totalBooks = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(quantity),0) FROM books")
    totalQuantity = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(available),0) FROM books")
    availableBooks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issued_books")
    issuedBooks = cur.fetchone()[0]

    conn.close()

    return jsonify({

        "books": books,
        "totalBooks": totalBooks,
        "totalQuantity": totalQuantity,
        "availableBooks": availableBooks,
        "issuedBooks": issuedBooks

    })


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5002)   