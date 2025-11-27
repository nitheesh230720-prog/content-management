from flask import Flask, render_template, request, session, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecretkey"

def connect_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    db = connect_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            userid TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

@app.route("/")
def index():
    return redirect("/login")

@app.route("/register")
def show_register():
    return render_template("index.html", page="register")

@app.route("/login")
def show_login():
    return render_template("index.html", page="login")

@app.route("/register", methods=["POST"])
def register_user():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    userid = request.form.get("userid")
    password = request.form.get("password")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE userid = ?", (userid,))
    existing_user = cursor.fetchone()

    if existing_user:
        db.close()
        return render_template("index.html", page="register", message="User ID already taken.")

    hashed_pw = generate_password_hash(password)
    cursor.execute("INSERT INTO users (fname, lname, userid, password) VALUES (?, ?, ?, ?)",
                   (fname, lname, userid, hashed_pw))
    db.commit()
    db.close()

    return render_template("index.html", page="login", message="Registration successful! Please log in.")

@app.route("/login", methods=["POST"])
def login_user():
    userid = request.form.get("userid")
    password = request.form.get("password")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE userid = ?", (userid,))
    user = cursor.fetchone()
    db.close()

    if user and check_password_hash(user["password"], password):
        session["userid"] = user["userid"]
        session["fname"] = user["fname"]
        session["lname"] = user["lname"]
        return render_template("index.html", page="home", fname=user["fname"], lname=user["lname"])

    return render_template("index.html", page="login", message="Wrong User ID or Password.")

@app.route("/logout")
def logout_user():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
