import os
import click
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, seed_db, create_user, get_user_by_email, get_user_by_id, update_user_name, update_user_password

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")


# ------------------------------------------------------------------ #
# CLI commands                                                        #
# ------------------------------------------------------------------ #

@app.cli.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialised.")


@app.cli.command("seed-db")
def seed_db_command():
    seed_db()
    click.echo("Database seeded.")


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        error = None
        if not name:
            error = "Full name is required."
        elif not email:
            error = "Email address is required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif get_user_by_email(email):
            error = "An account with that email already exists."

        if error:
            return render_template("register.html", error=error, name=name, email=email)

        user = create_user(name, email, generate_password_hash(password))
        session["user_id"] = user["id"]
        return redirect(url_for("landing"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.", email=email)

        session["user_id"] = user["id"]
        return redirect(url_for("landing"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("landing"))


def _profile_ctx(user_id):
    user = get_user_by_id(user_id)
    member_since = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")
    return user, member_since


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user, member_since = _profile_ctx(session["user_id"])
    return render_template("profile.html", user=user, member_since=member_since)


@app.route("/profile/name", methods=["POST"])
def profile_name():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    name = request.form.get("name", "").strip()
    user, member_since = _profile_ctx(session["user_id"])
    if not name:
        return render_template("profile.html", user=user, member_since=member_since,
                               name_error="Name cannot be empty.")
    update_user_name(session["user_id"], name)
    user, member_since = _profile_ctx(session["user_id"])
    return render_template("profile.html", user=user, member_since=member_since,
                           name_msg="Name updated successfully.")


@app.route("/profile/password", methods=["POST"])
def profile_password():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user, member_since = _profile_ctx(session["user_id"])
    current = request.form.get("current_password", "")
    new_pw  = request.form.get("new_password", "")
    confirm = request.form.get("confirm_password", "")

    def err(msg):
        return render_template("profile.html", user=user, member_since=member_since, pw_error=msg)

    if not check_password_hash(user["password_hash"], current):
        return err("Current password is incorrect.")
    if len(new_pw) < 8:
        return err("Password must be at least 8 characters.")
    if new_pw != confirm:
        return err("Passwords do not match.")

    update_user_password(session["user_id"], generate_password_hash(new_pw))
    user, member_since = _profile_ctx(session["user_id"])
    return render_template("profile.html", user=user, member_since=member_since,
                           pw_msg="Password changed successfully.")


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
