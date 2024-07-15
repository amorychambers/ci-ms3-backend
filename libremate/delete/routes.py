from flask import Blueprint, redirect, url_for, flash, session
from libremate import db
from libremate.models.models import Reader, Genre, Book

delete = Blueprint("delete", __name__)


@delete.route("/delete_genre/<int:genre_id>")
def delete_genre(genre_id):
    genre = db.session.query(Genre).get_or_404(genre_id)
    if genre.genre_name != "misc":
        db.session.delete(genre)
        db.session.commit()
        flash(f"'{genre.genre_name.capitalize()}' genre deleted")
    return redirect(url_for("library.my_library"))


@delete.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"'{book.book_title}' deleted")
    return redirect(url_for("library.my_library"))

@delete.route("/delete_account/<int:reader_id>")
def delete_account(reader_id):
    reader = db.session.query(Reader).filter(Reader.id == reader_id).one_or_none()
    db.session.delete(reader)
    db.session.commit()
    session.clear()
    flash("Account deleted. Goodnight and good luck!")
    return redirect(url_for("shared.community", page=1))