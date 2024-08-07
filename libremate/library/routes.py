from flask import Blueprint, render_template, session
from libremate import db
from libremate.models.models import Genre, Book

library = Blueprint("library", __name__)


@library.route("/my_library")
def my_library():
    if "user" in session:
        genres = db.session.query(Genre).order_by(Genre.genre_name).filter(
            Genre.genre_owner == session["user"]).all()
        books = db.session.query(Book).order_by(Book.book_title).filter(
            Book.book_owner == session["user"]).all()
        return render_template("my_library.html", genres=genres, books=books)
    else:
        return render_template("404.html")


@library.route("/my_library/sort_by/<sort>")
def my_library_sort(sort):
    genres = db.session.query(Genre).order_by(Genre.genre_name).filter(
        Genre.genre_owner == session["user"]).all()
    if sort == "created_on":
        books = db.session.query(Book).order_by(Book.created_on.desc()).filter(
            Book.book_owner == session["user"]).all()
    else:
        books = db.session.query(Book).order_by(sort).filter(
            Book.book_owner == session["user"]).all()
    status_options = ["complete", "plan-to-read", "dropped"]
    statuses = []
    for status in status_options:
        if len(db.session.query(Book).filter(
            Book.status == status and Book.book_owner == session["user"]
                ).all()) >= 1:
            statuses.append(status)
    return render_template("my_library.html",
                           genres=genres,
                           books=books,
                           sort=sort,
                           statuses=statuses)


@library.route("/view_book/<id>")
def view_book(id):
    book = db.session.query(Book).get_or_404(id)
    return render_template("view_book.html", book=book)
