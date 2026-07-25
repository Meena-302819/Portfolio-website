from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "portfolio_secret_key"

DATABASE = "portfolio.db"


# ======================================
# Database Connection
# ======================================

def get_db():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


# ======================================
# Create Database Tables
# ======================================

def create_tables():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT NOT NULL,

        subject TEXT NOT NULL,

        message TEXT NOT NULL,

        date TEXT NOT NULL

    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS visitors(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        visit_time TEXT NOT NULL

    )
    """)

    conn.commit()
    conn.close()


create_tables()


# ======================================
# Visitor Counter
# ======================================

def add_visitor():

    conn = get_db()

    cur = conn.cursor()

    cur.execute(

        "INSERT INTO visitors(visit_time) VALUES(?)",

        (

            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

        )

    )

    conn.commit()

    conn.close()


# ======================================
# Home Page
# ======================================

@app.route("/")
def home():

    add_visitor()

    return render_template("index.html")
# ======================================
# Contact Form
# ======================================

@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""

    INSERT INTO contacts(

        name,
        email,
        subject,
        message,
        date

    )

    VALUES(?,?,?,?,?)

    """,

    (

        name,
        email,
        subject,
        message,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    ))

    conn.commit()
    conn.close()

    flash("Message Sent Successfully!")

    return redirect(url_for("home"))


# ======================================
# Login Page
# ======================================

@app.route("/login")
def login():

    return render_template("login.html")


# ======================================
# Admin Dashboard
# ======================================

@app.route("/admin")
def admin():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM visitors")
    visitors = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM contacts")
    messages = cur.fetchone()[0]

    conn.close()

    return render_template(

        "admin.html",

        visitors=visitors,

        messages=messages

    )


# ======================================
# View Contact Messages
# ======================================

@app.route("/messages")
def messages():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM contacts

    ORDER BY id DESC

    """)

    contacts = cur.fetchall()

    conn.close()

    return render_template(

        "contact_messages.html",

        contacts=contacts

    )


# ======================================
# Delete Message
# ======================================

@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()

    cur = conn.cursor()

    cur.execute(

        "DELETE FROM contacts WHERE id=?",

        (id,)

    )

    conn.commit()

    conn.close()

    return redirect(url_for("messages"))
import os
from flask import send_from_directory

# ======================================
# Project Folder
# ======================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")


# ======================================
# Student Management
# ======================================

from flask import redirect

@app.route("/student-management")
def student_management():
    return redirect("http://127.0.0.1:5001")

@app.route("/library-management")
def library_management():
    return redirect("http://127.0.0.1:5002")

@app.route("/inventory-management")
def inventory_management():
    return redirect("http://127.0.0.1:5003")
# ======================================
# Run Flask
# ======================================

if __name__ == "__main__":

    app.run(
        debug=True
    )