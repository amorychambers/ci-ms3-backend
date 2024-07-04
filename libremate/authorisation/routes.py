from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from libremate import app
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import math

authorisation = Blueprint("authorisation", __name__)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists
        q = db.session.query(Reader).filter(
            Reader.username == request.form.get("username"))
        if db.session.query(q.exists()).scalar():
            flash("Username already taken")
            redirect(url_for("register"))
        else:
            session["user"] = request.form.get("username")
            reader = Reader(
                username=request.form.get("username"),
                password=generate_password_hash(
                    request.form.get("new-password")),
                private=bool(request.form.get("private"))
            )
            db.session.add(reader)
            db.session.commit()
            default_genre = Genre(
                genre_name="misc",
                genre_owner=request.form.get("username"))
            db.session.add(default_genre)
            db.session.commit()
            flash("Registration successful!")
            return redirect(url_for("my_library"))

    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # Check that username exists
        q = db.session.query(Reader).filter(
            Reader.username == request.form.get("username"))
        if db.session.query(q.exists()).scalar():
            # Check password is correct
            if check_password_hash(q.first().password, request.form.get("password")):
                session["user"] = q.first().username
                flash(f"Hello, {session["user"]}!")
                return redirect(url_for("my_library"))
            else:
                # Password is not correct
                flash("Incorrect Username and/or Password")
                return redirect(url_for("sign_in"))
        else:
            flash("Username does not exist")
            return redirect(url_for("sign_in"))
    return render_template("sign_in.html")


@app.route("/sign_out")
def sign_out():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("home"))