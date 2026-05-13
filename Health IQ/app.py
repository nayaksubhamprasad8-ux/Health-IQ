import csv
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "healthiq_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_NAME = "Health_IQ_Pure_Health_Plans_Detailed.csv"

def load_users():
    try:
        with open(os.path.join(BASE_DIR, "users.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading users:", e)
        return []

def save_users(users):
    with open(os.path.join(BASE_DIR, "users.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def load_plans():
    possible_paths = [
        os.path.join(BASE_DIR, CSV_NAME),
        os.path.join(BASE_DIR, "Data", CSV_NAME),
        os.path.join(BASE_DIR, "data", CSV_NAME),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    plans = list(csv.DictReader(f))
                    print(f"Loaded {len(plans)} plans from: {path}")
                    return plans
            except Exception as e:
                print("Error reading CSV:", e)
    print("CSV not found. Tried:", possible_paths)
    return []

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():
    users = load_users()
    email = request.form.get("email")
    password = request.form.get("password")
    for user in users:
        if user["email"] == email and user["password"] == password:
            session["user"] = user["name"]
            session["email"] = user["email"]
            return redirect(url_for("home"))
    return render_template("login.html", error="Invalid email or password")

@app.route("/signup", methods=["POST"])
def signup():
    users = load_users()
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    if any(u["email"] == email for u in users):
        return render_template("login.html", error="Email already exists")
    users.append({"name": name, "email": email, "password": password})
    save_users(users)
    session["user"] = name
    session["email"] = email
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

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
    print("Selected Plans:", selected_names)
    if len(selected_names) < 2 or len(selected_names) > 3:
        return render_template("compare.html", selected=[], error="Please select 2 or 3 plans to compare.")
    all_plans = load_plans()
    selected = [p for p in all_plans if p.get("Plan_Name") in selected_names]
    return render_template("compare.html", selected=selected, error=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
