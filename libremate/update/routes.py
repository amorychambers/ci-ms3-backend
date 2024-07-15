from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Genre, Book

update = Blueprint("update", __name__)


@update.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    genres = db.session.query(Genre).filter(Genre.genre_owner == session["user"]).all()
    book = db.session.query(Book).get_or_404(book_id)
    statuses = ["complete", "plan-to-read", "dropped"]
    if request.method == "POST":
        book.status = request.form.get("status")
        book.favourite = bool(request.form.get("favourite"))
        book.book_genre = request.form.get("book_genre")
        book.isbn = request.form.get("isbn")
        book.review = request.form.get("review")
        db.session.commit()
        return redirect(url_for("library.view_book", id=book.id))
    return render_template("edit_book.html", book=book, genres=genres, statuses=statuses)


@update.route("/edit_genre/<int:genre_id>", methods=["POST"])
def edit_genre(genre_id):
    genre = db.session.query(Genre).get_or_404(genre_id)
    if request.method == "POST" and genre.genre_name != "Misc" and genre.genre_owner == session["user"]:
        # Check if genre already exists
        q = db.session.query(Genre.id).filter(Genre.genre_owner == session["user"],
                                              Genre.genre_name == request.form.get("genre_name").lower())
        if db.session.query(q.exists()).scalar():
            flash("That genre already exists in your library!")
            return redirect(url_for("settings.account"))
        else:
            genre.genre_name = request.form.get("genre_name")
            db.session.commit()
            return redirect(url_for("settings.account"))
    else:
        flash("I'm sorry, but you cannot edit this genre name")
        return redirect(url_for("settings.account"))


@update.route("/save_books/<genre_id>", methods=["GET", "POST"])
def save_books(genre_id):
    books = db.session.query(Book).filter(Book.book_genre == genre_id).all()
    misc = db.session.query(Genre).filter(
        Genre.genre_name == "misc", Genre.genre_owner == session["user"]).one()
    for book in books:
        book.book_genre = misc.id
    db.session.commit()
    flash("Books saved under Misc")
    return redirect(url_for("settings.account"))
