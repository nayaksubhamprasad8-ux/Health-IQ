import csv
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "healthiq_secret"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_users():
    try:
        with open(os.path.join(BASE_DIR, "users.json")) as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(os.path.join(BASE_DIR, "users.json"), "w") as f:
        json.dump(users, f)

def load_plans():
    try:
        with open(os.path.join(BASE_DIR, "Data", "Health_IQ_60_Pure_Health_Plans_Detailed.csv")) as f:
            return list(csv.DictReader(f))
    except:
        return []

@app.route("/")
def index():
    return redirect(url_for("home" if "user" in session else "login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():
    users = load_users()
    email = request.form["email"]
    password = request.form["password"]
    for u in users:
        if u["email"] == email and u["password"] == password:
            session["user"] = u["name"]
            return redirect(url_for("home"))
    return render_template("login.html", error="Invalid email or password")

@app.route("/signup", methods=["POST"])
def signup():
    users = load_users()
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    if any(u["email"] == email for u in users):
        return render_template("login.html", error="Email already exists")
    users.append({"name": name, "email": email, "password": password})
    save_users(users)
    session["user"] = name
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/plans")
def plans():
    if "user" not in session:
        return redirect(url_for("login"))
    plans_list = load_plans()
    return render_template("plans.html", plans=plans_list)

@app.route("/compare")
def compare():
    if "user" not in session:
        return redirect(url_for("login"))
    selected_names = request.args.getlist("plans")
    all_plans = load_plans()
    selected = [p for p in all_plans if p["Plan_Name"] in selected_names]
    error = None
    if selected_names and (len(selected_names) < 2 or len(selected_names) > 3):
        error = "Please select 2 or 3 plans to compare."
    return render_template("compare.html", selected=selected, error=error)

if __name__ == "__main__":
    app.run(debug=True)