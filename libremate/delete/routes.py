from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Genre, Book

delete = Blueprint("delete", __name__)


@delete.route("/delete_genre/<int:genre_id>")
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if genre.genre_name != "misc":
        db.session.delete(genre)
        db.session.commit()
        flash(f"'{genre.genre_name.capitalize()}' genre deleted")
    return redirect(url_for("my_library"))


@delete.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"'{book.book_title}' deleted")
    return redirect(url_for("my_library"))

@delete.route("/delete_account")
def delete_account():
    reader = Reader.query.first_or_404(Reader.username == session["user"])
    db.session.delete(reader)
    db.session.commit()
    session.clear()
    flash("Account deleted. Goodnight and good luck!")
    return redirect(url_for("community.community", page=1))