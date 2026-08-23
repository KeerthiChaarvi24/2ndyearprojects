import sqlite3

connection = sqlite3.connect('database.db')

connection.execute(""" create table if not exists questions(
id integer primary key autoincrement,
question text not null,
option1 text not null,
option2 text not null,
option3 text not null,
option4 text not null,
answer text not null)""")

connection.execute(""" create table if not exists scores (
id integer primary key autoincrement,
name text not null,
score integer not null)""")

questions = [
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

for question in questions:
    connection.execute("insert into questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)", question)

connection.commit()
connection.close()
print("Questions inserted successfully.")