import hmac
import os
import sqlite3
from pathlib import Path

from flask import Flask, Response, abort, render_template, request

app = Flask(__name__)
DATABASE_PATH = os.environ.get(
    "SS_DATABASE_PATH",
    str(Path(__file__).resolve().parent / "ss_database.db"),
)

def get_db():
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_database():
    connection = get_db()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            college TEXT NOT NULL,
            year TEXT NOT NULL,
            interest TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/opportunities")
def opportunities():
    return render_template("opportunities.html")

@app.route("/ambassador")
def ambassador():
    return render_template("ambassador.html")

@app.route("/roles")
def roles():
    return render_template("roles.html")

@app.route("/divisions")
def divisions():
    return render_template("divisions.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/career")
def career():
    return render_template("career.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/talent")
def talent():
    return render_template("talent.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/learning")
def learning():
    return render_template("learning.html")

@app.route("/admin")
def admin():
    configured_username = os.environ.get("SS_ADMIN_USERNAME")
    configured_password = os.environ.get("SS_ADMIN_PASSWORD")
    credentials = request.authorization

    if not configured_username or not configured_password:
        abort(503, description="Admin access is not configured.")

    if (
        credentials is None
        or not hmac.compare_digest(credentials.username or "", configured_username)
        or not hmac.compare_digest(credentials.password or "", configured_password)
    ):
        return Response(
            "Authentication required",
            401,
            {"WWW-Authenticate": 'Basic realm="SS Admin Dashboard"'},
        )

    connection = get_db()
    try:
        students = connection.execute(
            "SELECT * FROM registrations ORDER BY id DESC"
        ).fetchall()
    finally:
        connection.close()

    return render_template("admin.html", students=students)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        college = request.form.get("college")
        year = request.form.get("year")
        interest = request.form.get("interest")
        message = request.form.get("message")

        connection = get_db()

        connection.execute(
            """
            INSERT INTO registrations
            (name, email, phone, college, year, interest, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, email, phone, college, year, interest, message)
        )

        connection.commit()
        connection.close()

        return render_template("success.html", name=name)

    return render_template("register.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

create_database()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
