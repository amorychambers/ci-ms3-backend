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
                genre_name=request.form.get("genre_name").lower(),
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
    books = list(db.session.query(Book).order_by(Book.created_on.desc()).join(Reader).filter(Reader.private == False).all())
    if len(books) == 0:
        page_numbers = 1
        current_group = []
    else:
        page_numbers = (math.ceil(len(books)/3))
        groups = [books[i:i+3] for i in range(0, len(books), 3)]
        current_group = groups[(int(page)-1)]
        session['page'] = int(page)
    return render_template("community.html", books=current_group, page_numbers=page_numbers)


@app.route("/delete_genre/<int:genre_id>")
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if genre.genre_name != "misc":
        db.session.delete(genre)
        db.session.commit()
    return redirect(url_for("my_library"))


@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("my_library"))


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    genres = Genre.query.filter(Genre.genre_owner == session["user"]).all()
    book = Book.query.get_or_404(book_id)
    statuses = [{"value": "plan-to-read", "desc": "Plan-to-read"},
                {"value": "complete", "desc": "Complete"},
                {"value": "dropped", "desc": "Dropped"}]
    if request.method == "POST" and book.book_owner == session["user"]:
        book.status = request.form.get("status")
        book.favourite = bool(request.form.get("favourite"))
        book.book_genre = request.form.get("book_genre")
        book.isbn = request.form.get("isbn")
        book.review = request.form.get("review")
        db.session.commit()
        return redirect(url_for("view_book", id=book.id))
    return render_template("edit_book.html", book=book, genres=genres, statuses=statuses)


@app.route("/edit_genre/<int:genre_id>", methods=["POST"])
def edit_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if genre.genre_name != "Misc" and request.method == "POST" and genre.genre_owner == session["user"]:
         # Check if genre already exists
        q = db.session.query(Genre.id).filter(Genre.genre_owner == session["user"],
                                              Genre.genre_name == request.form.get("genre_name").lower())
        if db.session.query(q.exists()).scalar():
            flash("That genre already exists in your library!")
            return redirect(url_for("account"))
        else:
            genre.genre_name = request.form.get("genre_name")
            db.session.commit()
            return redirect(url_for("account"))
    else:
        flash("I'm sorry, but you cannot edit this genre name")
        return redirect(url_for("account"))


@app.route("/account")
def account():
    genres = Genre.query.filter(Genre.genre_owner == session["user"]).all()
    reader = Reader.query.filter(Reader.username == session["user"]).one()
    return render_template("account.html", genres=genres, reader=reader)


@app.route("/account/privacy/<status>", methods=["GET", "POST"])
def privacy(status):
    reader = Reader.query.filter(Reader.username == session["user"]).one()
    if status == 'public':
        reader.private = False
        db.session.commit()
    else:
        reader.private = True
        db.session.commit()
    return redirect(url_for("account"))


@app.route("/delete_account")
def delete_account():
    reader = Reader.query.filter(Reader.username == session["user"]).one()
    db.session.delete(reader)
    db.session.commit()
    session.clear()
    return redirect(url_for("community/1"))