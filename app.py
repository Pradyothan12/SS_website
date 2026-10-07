import hmac
import os
import secrets
import sqlite3
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for

app = Flask(__name__)
IS_PRODUCTION = os.environ.get("FLASK_ENV", "").lower() == "production" or bool(os.environ.get("RENDER"))
SECRET_KEY = os.environ.get("SECRET_KEY")
if IS_PRODUCTION and not SECRET_KEY:
    raise RuntimeError("Set SECRET_KEY in the production environment.")
if IS_PRODUCTION and (not os.environ.get("SS_ADMIN_USERNAME") or not os.environ.get("SS_ADMIN_PASSWORD")):
    raise RuntimeError("Set SS_ADMIN_USERNAME and SS_ADMIN_PASSWORD in the production environment.")
app.secret_key = SECRET_KEY or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=IS_PRODUCTION,
)
DATABASE_PATH = os.environ.get(
    "SS_DATABASE_PATH",
    str(Path(__file__).resolve().parent / "ss_database.db"),
)
ADMIN_USERNAME = os.environ.get("SS_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("SS_ADMIN_PASSWORD", "ss-local-admin-2026")


def get_db():
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    with get_db() as connection:
        connection.execute(
            """
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
            """
        )


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


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if hmac.compare_digest(username, ADMIN_USERNAME) and hmac.compare_digest(password, ADMIN_PASSWORD):
            session.clear()
            session["admin_authenticated"] = True
            return redirect(url_for("admin"))
        return render_template("admin_login.html", error="Invalid username or password"), 401

    if not session.get("admin_authenticated"):
        return render_template("admin_login.html")

    with get_db() as connection:
        students = connection.execute(
            "SELECT * FROM registrations ORDER BY id DESC"
        ).fetchall()
    return render_template("admin.html", students=students)


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return redirect(url_for("admin"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    fields = ("name", "email", "phone", "college", "year", "interest")
    values = {field: request.form.get(field, "").strip() for field in fields}
    message = request.form.get("message", "").strip()
    if any(not value for value in values.values()):
        return render_template("register.html"), 400

    with get_db() as connection:
        connection.execute(
            """
            INSERT INTO registrations
            (name, email, phone, college, year, interest, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (*values.values(), message),
        )
    return render_template("success.html", name=values["name"])


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


create_database()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
