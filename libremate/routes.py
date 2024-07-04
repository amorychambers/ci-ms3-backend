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





@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
