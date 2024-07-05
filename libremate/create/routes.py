from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash
import datetime

create = Blueprint("create", __name__)

@create.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists
        q = db.session.query(Reader).filter(
            Reader.username == request.form.get("username"))
        if db.session.query(q.exists()).scalar():
            flash("Username already taken")
            return redirect(url_for("create.register"))
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
            return redirect(url_for("library.my_library"))

    return render_template("register.html")

@create.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    if request.method == "POST":
        # Check if genre already exists
        q = db.session.query(Genre.id).filter(Genre.genre_owner == session["user"],
                                              Genre.genre_name == request.form.get("genre_name").lower())
        if db.session.query(q.exists()).scalar():
            flash("That genre already exists in your library!")
            return redirect(url_for("create.add_genre"))
        else:
            genre = Genre(
                genre_name=request.form.get("genre_name").lower(),
                genre_owner=session["user"]
            )
            db.session.add(genre)
            db.session.commit()
            flash(f"'{genre.genre_name.capitalize()}' added to your genres")
            return redirect(url_for("library.my_library"))
    return render_template("add_genre.html")


@create.route("/add_book", methods=["GET", "POST"])
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
        return redirect(url_for("library.my_library"))
    return render_template("add_book.html", genres=genres)