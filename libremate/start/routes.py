from flask import Blueprint, render_template, redirect, url_for, session

start = Blueprint("start", __name__)


@start.route("/")
def home():
    if "user" in session:
        return redirect(url_for("library.my_library"))
    else:
        return redirect(url_for("authorisation.sign_in"))


@start.route("/about")
def about():
    return render_template("about.html")
