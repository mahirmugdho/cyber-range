from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # fine for local MVP only

DATABASE = "hospital.db"


def get_db_connection(): # type: ignore
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def login(): # type: ignore
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM staff WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            return redirect(url_for("patients"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/patients")
def patients():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    patients = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()

    return render_template("patients.html", patients=patients, user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)