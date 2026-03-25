import random
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

questions = [
    {"question": "Capital of India?", "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"], "answer": "Delhi"},
    {"question": "2 + 2 = ?", "options": ["3", "4", "5", "6"], "answer": "4"},
    {"question": "Largest planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Jupiter"},
    {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "High Text Machine", "Home Tool Markup", "None"], "answer": "Hyper Text Markup Language"},
    {"question": "Fastest animal?", "options": ["Cheetah", "Lion", "Tiger", "Horse"], "answer": "Cheetah"},
    {"question": "5 * 6 = ?", "options": ["30", "20", "25", "35"], "answer": "30"},
    {"question": "Python is developed by?", "options": ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark"], "answer": "Guido van Rossum"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        session["name"] = name
        session["score"] = 0
        session["q_index"] = 0

        # RANDOMIZE QUESTIONS
        session["questions"] = random.sample(questions, len(questions))

        return redirect("/quiz")
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = session.get("questions")

    if request.method == "POST":
        selected = request.form.get("answer")
        q_index = session["q_index"]

        if selected == questions[q_index]["answer"]:
            session["score"] += 1

        session["q_index"] += 1

    if session["q_index"] >= len(questions):
        return redirect("/result")

    question = questions[session["q_index"]]
    return render_template("quiz.html", question=question, q_num=session["q_index"]+1)

@app.route("/result")
def result():
    name = session.get("name")
    score = session.get("score")
    total = len(questions)

    # Save score
    with open("scores.txt", "a") as f:
        f.write(f"{name},{score}\n")

    return render_template("result.html", score=score, total=total)

@app.route("/leaderboard")
def leaderboard():
    scores = []

    with open("scores.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")

            # ✅ skip bad lines
            if len(parts) != 2:
                continue

            name, score = parts
            scores.append((name, int(score)))

    scores.sort(key=lambda x: x[1], reverse=True)

    return render_template("leaderboard.html", scores=scores)

if __name__ == "__main__":
    app.run(debug=True)