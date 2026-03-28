import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, session, Response
from psycopg2.extensions import connection as PGConnection

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

DB_CONFIG: dict[str, str] = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}

VULN_SQLI: bool = os.environ.get("VULN_SQLI", "false").lower() == "true"
VULN_DIR_TRAVERSAL: bool = os.environ.get("VULN_DIR_TRAVERSAL", "false").lower() == "true"


def get_db_connection() -> PGConnection:
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn


@app.route("/", methods=["GET", "POST"])
def login() -> Response | str:
    error: str | None = None

    if request.method == "POST":
        username: str = request.form.get("username", "")
        password: str = request.form.get("password", "")

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if VULN_SQLI:
            # Vulnerable: user input is interpolated directly into the query
            query = f"SELECT * FROM staff WHERE username = '{username}' AND password = '{password}'"
            cur.execute(query)
        else:
            # Safe: parameterized query prevents SQL injection
            cur.execute(
                "SELECT * FROM staff WHERE username = %s AND password = %s",
                (username, password)
            )

        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["user"] = user["username"]
            return redirect(url_for("patients"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/patients")
def patients() -> Response | str:
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM patients")
    all_patients = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("patients.html", patients=all_patients, user=session["user"])


@app.route("/files")
def files() -> tuple[str, int, dict[str, str]] | tuple[str, int]:
    if "user" not in session:
        return redirect(url_for("login"))

    filename: str = request.args.get("name", "")

    if VULN_DIR_TRAVERSAL:
        # Vulnerable: filename is used directly with no sanitization
        base_path = "/app/files"
        filepath = os.path.join(base_path, filename)
        try:
            with open(filepath, "r") as f:
                return f.read(), 200, {"Content-Type": "text/plain"}
        except FileNotFoundError:
            return "File not found.", 404
        except PermissionError:
            return "Permission denied.", 403
    else:
        return "File access is disabled.", 403


@app.route("/logout")
def logout() -> Response:
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)