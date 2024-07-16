from flask import Blueprint, render_template, session
from libremate import db
from libremate.models.models import Reader, Book
import math

shared = Blueprint("shared", __name__)


@shared.route("/community/<page>")
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
    return render_template("community.html",
                           books=current_group, page_numbers=page_numbers)
