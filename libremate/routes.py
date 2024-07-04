from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import math


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
