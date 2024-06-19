from flask import render_template, request, redirect, url_for, flash, session
from libremate import app, db
from libremate.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash, check_password_hash
import datetime, math


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists
        q = db.session.query(Reader.id).filter(
            Reader.username == request.form.get("username").lower())
        if db.session.query(q.exists()).scalar():
            flash("Username already taken")
            redirect(url_for("register"))
        else:
            session["user"] = request.form.get("username").lower()
            reader = Reader(
                username=request.form.get("username").lower(),
                password=generate_password_hash(
                    request.form.get("new-password")),
                private=bool(request.form.get("private"))
            )
            db.session.add(reader)
            db.session.commit()
            default_genre = Genre(
                genre_name="misc",
                genre_owner=request.form.get("username").lower())
            db.session.add(default_genre)
            db.session.commit()
            flash("Registration successful!")
            return redirect(url_for("my_library"))

    return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Check that username exists
        q = db.session.query(Reader).filter(
            Reader.username == request.form.get("username").lower())
        if db.session.query(q.exists()).scalar():
            # Check password is correct
            if check_password_hash(q.first().password, request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash(f"Hello, {session["user"]}!")
                return redirect(url_for("my_library"))
            else:
                # Password is not correct
                flash("Incorrect Username and/or Password")
                return redirect(url_for("signin"))
        else:
            flash("Username does not exist")
            return redirect(url_for("signin"))
    return render_template("signin.html")


@app.route("/signout")
def signout():
    session.clear()
    flash("You have been logged out")
    return render_template("base.html")


@app.route("/my_library")
def my_library():
    genres = Genre.query.order_by(Genre.genre_name).filter(Genre.genre_owner == session["user"]).all()
    books = Book.query.order_by(Book.book_title).filter(Book.book_owner == session["user"]).all()
    return render_template("my_library.html", genres=genres, books=books)

@app.route("/view_book/<id>", methods=["GET", "POST"])
def view_book(id):
    book = Book.query.filter(Book.id == id).one()
    return render_template("view_book.html", book=book)


@app.route("/add_genre", methods=["GET", "POST"])
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
                genre_name=request.form.get("genre_name"),
                genre_owner=session["user"]
            )
            db.session.add(genre)
            db.session.commit()
            return redirect(url_for("my_library"))
    return render_template("add_genre.html")


@app.route("/add_book", methods=["GET", "POST"])
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
        return redirect(url_for("my_library"))
    return render_template("add_book.html", genres=genres)

@app.route("/community/<page>")
def community(page):
    books = list(db.session.query(Book).join(Reader).filter(Reader.private == False).all())
    page_numbers = (math.ceil(len(books)/3))
    session['page'] = int(page)
    return render_template("community.html", books=books, page_numbers=page_numbers)