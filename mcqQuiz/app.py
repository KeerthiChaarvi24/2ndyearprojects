from flask import Flask, render_template, redirect, request, session
import sqlite3
import os
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "solvify-secret-key")

QUIZ_TIME = 10 * 60
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "solvifyadmin")


def get_connection():
    return sqlite3.connect("database/database.db")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz", methods=["POST"])
def quiz():
    username = request.form["username"]

    connection = get_connection()
    questions = connection.execute("select * from questions").fetchall()
    connection.close()

    session["quiz_start"] = time.time()

    return render_template(
        "quiz.html",
        username=username,
        questions=questions
    )


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]

    start_time = session.get("quiz_start")

    if start_time and time.time() - start_time > QUIZ_TIME + 5:
        score = 0
    else:
        score = 0

        connection = get_connection()
        questions = connection.execute(
            "select * from questions"
        ).fetchall()

        for question in questions:
            user_answer = request.form.get(
                f"question_{question[0]}"
            )

            if user_answer == question[6]:
                score += 1

        connection.execute(
            "insert into scores (name, score) values (?, ?)",
            (username, score)
        )

        connection.commit()
        connection.close()

    session.pop("quiz_start", None)

    return render_template(
        "result.html",
        username=username,
        score=score
    )


@app.route("/leaderboard")
def leaderboard():
    connection = get_connection()

    scores = connection.execute(
        "select name, score from scores order by score DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "leaderboard.html",
        scores=scores
    )


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]

        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")

        return render_template(
            "admin_login.html",
            error="WRONG PASSWORD!"
        )

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin/login")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin/login")

    connection = get_connection()

    questions = connection.execute(
        "select * from questions"
    ).fetchall()

    scores = connection.execute(
        "select name, score from scores order by score DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        questions=questions,
        scores=scores
    )


@app.route("/admin/add", methods=["POST"])
def add_question():
    if not session.get("admin"):
        return redirect("/admin/login")

    question = request.form["question"]
    option1 = request.form["option1"]
    option2 = request.form["option2"]
    option3 = request.form["option3"]
    option4 = request.form["option4"]
    answer = request.form["answer"]

    connection = get_connection()

    connection.execute(
        """insert into questions
        (question, option1, option2, option3, option4, answer)
        values (?, ?, ?, ?, ?, ?)""",
        (
            question,
            option1,
            option2,
            option3,
            option4,
            answer
        )
    )

    connection.commit()
    connection.close()

    return redirect("/admin")


@app.route("/admin/delete/<int:id>", methods=["POST"])
def delete_question(id):
    if not session.get("admin"):
        return redirect("/admin/login")

    connection = get_connection()

    connection.execute(
        "delete from questions where id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)