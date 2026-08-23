from flask import Flask, render_template,redirect,request
import sqlite3
app= Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz",methods=["POST"])
def quiz():
    username=request.form["username"]
    connection = sqlite3.connect('database.db')
    questions = connection.execute("select * from questions").fetchall()
    connection.close()

    return render_template("quiz.html", username=username, questions=questions)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    score = 0
    connection = sqlite3.connect('database.db')
    questions = connection.execute("select * from questions").fetchall()

    for question in questions:
        user_answer = request.form.get(f"question_{question[0]}")
        if user_answer == question[6]:  # question[6] is the correct answer
            score += 1

    connection.execute("insert into scores (name, score) VALUES (?, ?)", (username, score))
    connection.commit()
    connection.close()
    return render_template("result.html", username=username, score=score)

@app.route("/leaderboard")
def leaderboard():
    connection = sqlite3.connect("database.db")
    score = connection.execute(
        "SELECT name, score FROM scores ORDER BY score DESC"
    ).fetchall()
    connection.close()
    return render_template("leaderboard.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)