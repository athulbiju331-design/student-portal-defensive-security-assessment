from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, abort, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from pathlib import Path
import sqlite3
import secrets
import time
import logging

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "student_portal.db"
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # Local HTTP only; use True with HTTPS in production
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
)

logging.basicConfig(
    filename=BASE_DIR / "security.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}

login_attempts = {}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'admin'))
        );

        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)

    admin = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if not admin:
        conn.execute(
            """
            INSERT INTO users
            (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (
                "admin",
                generate_password_hash("AdminDemo123!"),
                "admin"
            )
        )

    student = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        ("student",)
    ).fetchone()

    if not student:
        conn.execute(
            """
            INSERT INTO users
            (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (
                "student",
                generate_password_hash("StudentDemo123!"),
                "student"
            )
        )

    conn.commit()
    conn.close()


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)

    return session["csrf_token"]


@app.context_processor
def inject_csrf():
    return {"csrf_token": csrf_token}


def validate_csrf():
    token = request.form.get("csrf_token", "")

    if not secrets.compare_digest(
        token,
        session.get("csrf_token", "")
    ):
        abort(400, description="Invalid CSRF token")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)

        return view(*args, **kwargs)

    return wrapped


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def rate_limited(username):
    now = time.time()

    attempts = [
        t
        for t in login_attempts.get(username, [])
        if now - t < 60
    ]

    login_attempts[username] = attempts

    return len(attempts) >= 5


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )

    return response


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        validate_csrf()

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if len(username) < 3 or len(username) > 30:
            flash(
                "Username must be between 3 and 30 characters."
            )

            return redirect(
                url_for("register")
            )

        if len(password) < 10:
            flash(
                "Password must contain at least 10 characters."
            )

            return redirect(
                url_for("register")
            )

        try:

            conn = get_db()

            conn.execute(
                """
                INSERT INTO users
                (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (
                    username,
                    generate_password_hash(password),
                    "student"
                )
            )

            conn.commit()
            conn.close()

            logging.info(
                "Registration successful username=%s",
                username
            )

            flash(
                "Registration successful. Please log in."
            )

            return redirect(
                url_for("login")
            )

        except sqlite3.IntegrityError:

            flash(
                "Username already exists."
            )

            return redirect(
                url_for("register")
            )

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        validate_csrf()

        username = request.form.get(
            "username",
            ""
        ).strip()

        if rate_limited(username):

            logging.warning(
                "Login rate limit username=%s",
                username
            )

            flash(
                "Too many login attempts. Please wait one minute."
            )

            return redirect(
                url_for("login")
            )

        login_attempts.setdefault(
            username,
            []
        ).append(time.time())

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if (
            user
            and check_password_hash(
                user["password_hash"],
                request.form.get("password", "")
            )
        ):

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["csrf_token"] = secrets.token_urlsafe(32)

            logging.info(
                "Login success username=%s role=%s",
                user["username"],
                user["role"]
            )

            return redirect(
                url_for("dashboard")
            )

        logging.warning(
            "Login failure username=%s",
            username
        )

        flash(
            "Invalid username or password."
        )

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():

    validate_csrf()

    username = session.get(
        "username"
    )

    session.clear()

    logging.info(
        "Logout username=%s",
        username
    )

    return redirect(
        url_for("home")
    )


@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db()

    user = conn.execute(
        """
        SELECT id, username, role
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    assignments = conn.execute(
        """
        SELECT *
        FROM assignments
        WHERE user_id = ?
        ORDER BY submitted_at DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        assignments=assignments
    )


@app.route("/submit-assignment", methods=["POST"])
@login_required
def submit_assignment():

    validate_csrf()

    uploaded = request.files.get(
        "assignment"
    )

    if not uploaded or not uploaded.filename:

        flash(
            "Please select a file."
        )

        return redirect(
            url_for("dashboard")
        )

    original_name = secure_filename(
        uploaded.filename
    )

    if (
        not original_name
        or not allowed_file(original_name)
    ):

        flash(
            "Allowed file types: PDF, DOC, DOCX, TXT."
        )

        logging.warning(
            "Blocked file upload username=%s filename=%s",
            session.get("username"),
            uploaded.filename
        )

        return redirect(
            url_for("dashboard")
        )

    stored_name = (
        f"{secrets.token_hex(16)}_{original_name}"
    )

    uploaded.save(
        UPLOAD_DIR / stored_name
    )

    conn = get_db()

    conn.execute(
        """
        INSERT INTO assignments
        (user_id, filename, original_name)
        VALUES (?, ?, ?)
        """,
        (
            session["user_id"],
            stored_name,
            original_name
        )
    )

    conn.commit()
    conn.close()

    logging.info(
        "Assignment uploaded username=%s filename=%s",
        session.get("username"),
        original_name
    )

    flash(
        "Assignment uploaded successfully."
    )

    return redirect(
        url_for("dashboard")
    )


@app.route("/admin")
@login_required
@admin_required
def admin():

    conn = get_db()

    users = conn.execute(
        """
        SELECT id, username, role
        FROM users
        ORDER BY id
        """
    ).fetchall()

    assignments = conn.execute(
        """
        SELECT
            assignments.id,
            assignments.original_name,
            assignments.submitted_at,
            users.username
        FROM assignments
        JOIN users
            ON assignments.user_id = users.id
        ORDER BY assignments.submitted_at DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        assignments=assignments
    )


@app.route("/uploads/<path:filename>")
@login_required
def download_upload(filename):

    conn = get_db()

    item = conn.execute(
        "SELECT * FROM assignments WHERE filename = ?",
        (filename,)
    ).fetchone()

    conn.close()

    if not item:
        abort(404)

    if (
        session.get("role") != "admin"
        and item["user_id"] != session["user_id"]
    ):
        abort(403)

    return send_from_directory(
        UPLOAD_DIR,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":

    init_db()

    # Debug disabled for the Task 5 defensive assessment.
    app.run(debug=False)