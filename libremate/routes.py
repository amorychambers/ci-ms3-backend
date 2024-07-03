from flask import render_template, request, redirect, url_for, flash, session
from libremate import app, db
from libremate.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import math


@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("my_library"))
    else:
        return redirect(url_for("sign_in"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists
        q = db.session.query(Reader).filter(
            Reader.username == request.form.get("username"))
        if db.session.query(q.exists()).scalar():
            flash("Username already taken")
            redirect(url_for("register"))
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
            return redirect(url_for("my_library"))

    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # Check that username exists
        q = db.session.query(Reader).filter(
            Reader.username == request.form.get("username"))
        if db.session.query(q.exists()).scalar():
            # Check password is correct
            if check_password_hash(q.first().password, request.form.get("password")):
                session["user"] = q.first().username
                flash(f"Hello, {session["user"]}!")
                return redirect(url_for("my_library"))
            else:
                # Password is not correct
                flash("Incorrect Username and/or Password")
                return redirect(url_for("sign_in"))
        else:
            flash("Username does not exist")
            return redirect(url_for("sign_in"))
    return render_template("sign_in.html")


@app.route("/sign_out")
def sign_out():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("home"))


@app.route("/my_library")
def my_library():
    genres = Genre.query.order_by(Genre.genre_name).filter(
        Genre.genre_owner == session["user"]).all()
    books = Book.query.order_by(Book.book_title).filter(
        Book.book_owner == session["user"]).all()
    return render_template("my_library.html", genres=genres, books=books)


@app.route("/my_library/sort_by/<sort>")
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


@app.route("/view_book/<id>", methods=["GET", "POST"])
def view_book(id):
    book = Book.query.get_or_404(id)
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
            flash(f"'{genre.genre_name.capitalize()}' added to your genres")
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
        flash(f"'{book.book_title}' added to your bookshelf!")
        return redirect(url_for("my_library"))
    return render_template("add_book.html", genres=genres)


@app.route("/community/<page>")
def community(page):
    books = list(db.session.query(Book).order_by(Book.created_on.desc()).join(
        Reader).filter(Reader.private == False).all())
    if len(books) == 0:
        page_numbers = 1
        current_group = []
        session["page"] = 1
    else:
        page_numbers = (math.ceil(len(books)/3))
        groups = [books[i:i+3] for i in range(0, len(books), 3)]
        current_group = groups[(int(page)-1)]
        session['page'] = int(page)
    return render_template("community.html", books=current_group, page_numbers=page_numbers)


@app.route("/save_books/<genre_id>", methods=["GET", "POST"])
def save_books(genre_id):
    books = Book.query.filter(Book.book_genre == genre_id).all()
    misc = Genre.query.filter(
        Genre.genre_name == "misc", Genre.genre_owner == session["user"]).one()
    for book in books:
        book.book_genre = misc.id
    db.session.commit()
    flash("Books saved under Misc")
    return redirect(url_for("account"))


@app.route("/delete_genre/<int:genre_id>")
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if genre.genre_name != "misc":
        db.session.delete(genre)
        db.session.commit()
        flash(f"'{genre.genre_name.capitalize()}' genre deleted")
    return redirect(url_for("my_library"))


@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"'{book.book_title}' deleted")
    return redirect(url_for("my_library"))


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    genres = Genre.query.filter(Genre.genre_owner == session["user"]).all()
    book = Book.query.get_or_404(book_id)
    statuses = ["complete", "plan-to-read", "dropped"]
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
    if request.method == "POST" and genre.genre_name != "Misc" and genre.genre_owner == session["user"]:
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
    reader = Reader.query.first_or_404(Reader.username == session["user"])
    return render_template("account.html", genres=genres, reader=reader)


@app.route("/account/privacy/<status>", methods=["GET", "POST"])
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


@app.route("/delete_account")
def delete_account():
    reader = Reader.query.first_or_404(Reader.username == session["user"])
    db.session.delete(reader)
    db.session.commit()
    session.clear()
    flash("Account deleted. Goodnight and good luck!")
    return redirect(url_for("community", page=1))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
