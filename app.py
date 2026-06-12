from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os

# If running on Vercel, save the database to the writable /tmp directory
if os.environ.get('VERCEL'):
    DB_NAME = '/tmp/bookings.db'
else:
    DB_NAME = 'bookings.db'  # Keeps it local for your computer

app = Flask(__name__)


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, subject, message]):
        return "Missing fields", 400

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO bookings (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        """, (name, email, subject, message))
        conn.commit()

    return redirect("/")


@app.route("/admin")
def admin():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM bookings ORDER BY id DESC")
        rows = c.fetchall()

    return render_template("admin.html", bookings=rows)


@app.route('/googlef09145e424d6740b.html')
def google_verify():
    return send_from_directory('.', 'googlef09145e424d6740b.html')


if __name__ == "__main__":
    app.run(debug=True)