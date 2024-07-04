from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Genre, Book
import datetime

library = Blueprint("library", __name__)

@library.route("/my_library")
def my_library():
    genres = Genre.query.order_by(Genre.genre_name).filter(
        Genre.genre_owner == session["user"]).all()
    books = Book.query.order_by(Book.book_title).filter(
        Book.book_owner == session["user"]).all()
    return render_template("my_library.html", genres=genres, books=books)


@library.route("/my_library/sort_by/<sort>")
def my_library_sort(sort):
    genres = Genre.query.order_by(Genre.genre_name).filter(
        Genre.genre_owner == session["user"]).all()
    if sort == "created_on":
        books = Book.query.order_by(Book.created_on.desc()).filter(
            Book.book_owner == session["user"]).all()
    else:
        books = Book.query.order_by(sort).filter(
            Book.book_owner == session["user"]).all()
    status_options = ["complete", "plan-to-read", "dropped"]
    statuses = []
    for status in status_options:
        if len(Book.query.filter(Book.status == status and Book.book_owner == session["user"]).all()) >= 1:
            statuses.append(status)
    return render_template("my_library.html", genres=genres, books=books, sort=sort, statuses=statuses)

@library.route("/view_book/<id>", methods=["GET", "POST"])
def view_book(id):
    book = Book.query.get_or_404(id)
    return render_template("view_book.html", book=book)


@library.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    if request.method == "POST":
        # Check if genre already exists
        q = db.session.query(Genre.id).filter(Genre.genre_owner == session["user"],
                                              Genre.genre_name == request.form.get("genre_name").lower())
        if db.session.query(q.exists()).scalar():
            flash("That genre already exists in your library!")
            return redirect(url_for("add_genre"))
        else:
            genre = Genre(
                genre_name=request.form.get("genre_name").lower(),
                genre_owner=session["user"]
            )
            db.session.add(genre)
            db.session.commit()
            flash(f"'{genre.genre_name.capitalize()}' added to your genres")
            return redirect(url_for("my_library"))
    return render_template("add_genre.html")


@library.route("/add_book", methods=["GET", "POST"])
def add_book():
    genres = Genre.query.filter(Genre.genre_owner == session["user"]).all()
    if request.method == "POST":
        book = Book(
            book_title=request.form.get("book_title"),
            author_name=request.form.get("author_name"),
            status=request.form.get("status"),
            favourite=bool(request.form.get("favourite")),
            created_on=(datetime.datetime.now().strftime("%x %X")),
            book_genre=request.form.get("book_genre"),
            isbn=request.form.get("isbn"),
            review=request.form.get("review"),
            book_owner=session["user"]
        )
        db.session.add(book)
        db.session.commit()
        flash(f"'{book.book_title}' added to your bookshelf!")
        return redirect(url_for("my_library"))
    return render_template("add_book.html", genres=genres)