from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Reader
from werkzeug.security import check_password_hash

authorisation = Blueprint("authorisation", __name__)


@authorisation.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # Check that username exists
        q = db.session.query(Reader).filter(
            Reader.username == request.form.get("username"))
        if db.session.query(q.exists()).scalar():
            # Check password is correct
            if check_password_hash(q.first().password,
                                   request.form.get("password")):
                session["user"] = q.first().username
                flash(f"Hello, {session["user"]}!")
                return redirect(url_for("library.my_library"))
            else:
                # Password is not correct
                flash("Incorrect Username and/or Password")
                return redirect(url_for("authorisation.sign_in"))
        else:
            flash("Username does not exist")
            return redirect(url_for("authorisation.sign_in"))
    return render_template("sign_in.html")


@authorisation.route("/sign_out")
def sign_out():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("start.home"))
