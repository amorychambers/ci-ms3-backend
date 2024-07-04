from flask import Blueprint, render_template, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Reader, Genre

account = Blueprint("account", __name__)

@account.route("/account")
def account():
    genres = Genre.query.filter(Genre.genre_owner == session["user"]).all()
    reader = Reader.query.first_or_404(Reader.username == session["user"])
    return render_template("account.html", genres=genres, reader=reader)


@account.route("/account/privacy/<status>", methods=["GET", "POST"])
def privacy(status):
    reader = Reader.query.first_or_404(Reader.username == session["user"])
    if status == "public":
        reader.private = False
        db.session.commit()
        flash("Account set to Public")
    else:
        reader.private = True
        db.session.commit()
        flash("Account set to Private")
    return redirect(url_for("account"))
