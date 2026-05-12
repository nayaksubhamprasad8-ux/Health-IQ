import csv
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "healthiq_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================
# LOAD & SAVE USERS
# =========================
def load_users():
    try:
        with open(os.path.join(BASE_DIR, "users.json"), "r") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(os.path.join(BASE_DIR, "users.json"), "w") as f:
        json.dump(users, f, indent=4)


# =========================
# LOAD HEALTH PLANS CSV
# =========================
def load_plans():
    try:
        with open(
            os.path.join(BASE_DIR, "Health_IQ_Pure_Health_Plans_Detailed.csv"),
            "r",
            encoding="utf-8",
        ) as f:
            return list(csv.DictReader(f))
    except:
        return []


# =========================
# ROOT ROUTE
# Always open login page first
# =========================
@app.route("/")
def index():
    return redirect(url_for("login"))


# =========================
# LOGIN PAGE
# =========================
@app.route("/login")
def login():
    return render_template("login.html")


# =========================
# SIGN IN
# =========================
@app.route("/signin", methods=["POST"])
def signin():

    users = load_users()

    email = request.form.get("email")
    password = request.form.get("password")

    for user in users:

        if user["email"] == email and user["password"] == password:

            # Store session
            session["user"] = user["name"]
            session["email"] = user["email"]

            return redirect(url_for("home"))

    return render_template(
        "login.html",
        error="Invalid email or password"
    )


# =========================
# SIGN UP
# =========================
@app.route("/signup", methods=["POST"])
def signup():

    users = load_users()

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Check duplicate email
    if any(u["email"] == email for u in users):

        return render_template(
            "login.html",
            error="Email already exists"
        )

    # Create new user
    new_user = {
        "name": name,
        "email": email,
        "password": password
    }

    users.append(new_user)

    save_users(users)

    # Create session
    session["user"] = name
    session["email"] = email

    return redirect(url_for("home"))


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# HOME PAGE
# =========================
@app.route("/home")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        user=session["user"]
    )


# =========================
# PLANS PAGE
# =========================
@app.route("/plans")
def plans():

    if "user" not in session:
        return redirect(url_for("login"))

    plans_list = load_plans()

    return render_template(
        "plans.html",
        plans=plans_list
    )


# =========================
# COMPARE PAGE
# =========================
@app.route("/compare")
def compare():

    if "user" not in session:
        return redirect(url_for("login"))

    selected_names = request.args.getlist("plans")

    all_plans = load_plans()

    selected = [
        p for p in all_plans
        if p["Plan_Name"] in selected_names
    ]

    error = None

    # Validation
    if selected_names:

        if len(selected_names) < 2 or len(selected_names) > 3:

            error = "Please select 2 or 3 plans to compare."

    return render_template(
        "compare.html",
        selected=selected,
        error=error
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
