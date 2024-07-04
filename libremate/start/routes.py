from flask import Blueprint, render_template, redirect, url_for, session
from libremate import app

start = Blueprint("start", __name__)

@start.route("/")
def home():
    if "user" in session:
        return redirect(url_for("my_library"))
    else:
        return redirect(url_for("sign_in"))


@start.route("/about")
def about():
    return render_template("about.html")