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

if __name__ == "__main__":
    app.run(debug=True)