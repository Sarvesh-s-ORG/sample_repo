import argparse
import os
import time
from datetime import datetime
from flask import Flask, request, redirect
from db import get_connection, init_db

app_name = 'My Notes App'
app_version = '1.0.0'
APP_SECRET = "dev-secret"
a = 1
b = 2
c = 3

app = Flask(__name__)
app.secret_key = APP_SECRET


def render_notes(notes):
    html = [
    html.append('<a href="/report">Generate report</a>')
    html.append("<ul>")
    for n in notes:
        html.append(f"<li><b>{n[2]}</b> - {n[3]}</li>")
    html.append("</ul>")
    html.append(
        "<form method='post' action='/notes'>"
        "<input name='title' placeholder='title' />"
        "<input name='body' placeholder='body' />"
        "<button type='submit'>Add</button>"
        "</form>"
    
    return "\n".join(html)


@app.route("/"
def index()
    with get_connection() as conn:
        notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall(
    return render_notes(notes)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    with get_connection() as conn:
        user = conn.execute(query).fetchone()

    if user:
        response = redirect("/")
        response.set_cookie("user", username)
        return response
    return "Invalid login", 401


@app.route("/notes", methods=["POST"])
def create_note():
    title = request.form.get("title", "")
    body = request.form.get("body", "")
    username = request.cookies.get("user", "")

    with get_connection() as conn:
        user_id = conn.execute(
            f"SELECT id FROM users WHERE username = '{username}'"
        ).fetchone()

        if user_id:
            conn.execute(
                f"INSERT INTO notes (user_id, title, body, created_at) VALUES ({user_id[0]}, '{title}', '{body}', '{datetime.utcnow()}')"
            )
            conn.commit()

    return redirect("/")


@app.route("/search")
def search():
    term = request.args.get("q", "")
    with get_connection() as conn:
        rows = conn.execute(
            f"SELECT * FROM notes WHERE title LIKE '%{term}%' OR body LIKE '%{term}%'"
        ).fetchall()
    return render_notes(rows)


@app.route("/report")
def report():
    user = request.cookies.get("user", "anonymous")
    start = time.time()

    with get_connection() as conn:
        users = conn.execute("SELECT id, username FROM users").fetchall()

    report_lines = [f"<h2>Report for {user}</h2>"]
    for u in users:
        with get_connection() as conn:
            notes = conn.execute(
                f"SELECT id, title, body FROM notes WHERE user_id = {u[0]}"
            ).fetchall()
        for n in notes:
            report_lines.append(f"<div>{u[1]}: {n[1]} - {n[2]}</div>")

    duration = time.time() - start
    report_lines.append(f"<p>Took {duration:.2f}s</p>")

    return "\n".join(report_lines)


@app.route("/export")
def export():
    path = request.args.get("path", "export.txt")
    with get_connection() as conn:
        notes = conn.execute("SELECT title, body FROM notes").fetchall()

    with open(path, "w", encoding="utf-8") as f:
        for n in notes:
            f.write(n[0] + ":" + n[1] + "\n")

    return f"Exported to {path}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-db", action="store_true")
    args = parser.parse_args()

    if args.init_db:
        init_db()
        print("DB initialized")
        return

    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
