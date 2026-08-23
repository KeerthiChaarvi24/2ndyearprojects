from flask import Flask, render_template, redirect, request, session
import psycopg2
import os
import time

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "solvify-secret-key")

QUIZ_TIME = 10 * 60
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "solvifyadmin")

questions_data = [
    (
        "What does HTML stand for?",
        "Hyper Text Markup Language",
        "High Text Machine Language",
        "Hyperlink Text Management Language",
        "Home Tool Markup Language",
        "A"
    ),
    (
        "Which language is mainly used to style a web page?",
        "HTML",
        "CSS",
        "Python",
        "SQL",
        "B"
    ),
    (
        "Which language is commonly used to add interactivity to web pages?",
        "HTML",
        "CSS",
        "JavaScript",
        "SQL",
        "C"
    ),
    (
        "Which language are we using to build the backend of our quiz?",
        "Python",
        "HTML",
        "CSS",
        "SQL",
        "A"
    ),
    (
        "Which SQL command is used to retrieve data from a table?",
        "INSERT",
        "DELETE",
        "SELECT",
        "CREATE",
        "C"
    ),
    (
        "What is Git mainly used for?",
        "Creating databases",
        "Version control",
        "Styling websites",
        "Running Python programs",
        "B"
    ),
    (
        "What does HTTP mainly define?",
        "How web browsers and servers communicate",
        "How computers store electricity",
        "How databases calculate scores",
        "How CSS styles are created",
        "A"
    ),
    (
        "What does a primary key do in a database table?",
        "Stores only text",
        "Uniquely identifies each row",
        "Deletes duplicate tables",
        "Connects to the internet",
        "B"
    ),
    (
        "Which data structure stores items in an ordered collection in Python?",
        "List",
        "Database",
        "Table",
        "Server",
        "A"
    ),
    (
        "What does CSS stand for?",
        "Computer Style System",
        "Cascading Style Sheets",
        "Creative Styling Syntax",
        "Coded Style Structure",
        "B"
    )
]


def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
            INSERT INTO questions
            (question, option1, option2, option3, option4, answer)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, questions_data)

    connection.commit()
    cursor.close()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz", methods=["POST"])
def quiz():
    username = request.form["username"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    cursor.close()
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
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()

        score = 0

        for question in questions:
            user_answer = request.form.get(
                f"question_{question[0]}"
            )

            if user_answer == question[6]:
                score += 1

        cursor.execute(
            "INSERT INTO scores (name, score) VALUES (%s, %s)",
            (username, score)
        )

        connection.commit()
        cursor.close()
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
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name, score FROM scores ORDER BY score DESC"
    )

    scores = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "leaderboard.html",
        scores=scores
    )


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


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    cursor.execute(
        "SELECT name, score FROM scores ORDER BY score DESC"
    )
    scores = cursor.fetchall()

    cursor.close()
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

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO questions
        (question, option1, option2, option3, option4, answer)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        request.form["question"],
        request.form["option1"],
        request.form["option2"],
        request.form["option3"],
        request.form["option4"],
        request.form["answer"]
    ))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/admin")


@app.route("/admin/delete/<int:id>", methods=["POST"])
def delete_question(id):
    if not session.get("admin"):
        return redirect("/admin/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM questions WHERE id = %s",
        (id,)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/admin")


initialize_database()

if __name__ == "__main__":
    app.run(debug=True)