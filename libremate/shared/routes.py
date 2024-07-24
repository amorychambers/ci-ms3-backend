from flask import Blueprint, render_template, session, request
from libremate import db
from libremate.models.models import Reader, Book
import math

shared = Blueprint("shared", __name__)


@shared.route("/community/<page>", methods=["GET", "POST"])
@shared.route("/community/<page>/<search>", methods=["GET", "POST"])
def community(page, search=None):
    if request.method == "POST":
        search = request.form.get("search_term")
        books = list(db.session.query(Book).order_by(Book.created_on.desc()).filter(
            Book.book_title.contains(search)).join(
            Reader).filter(Reader.private == False).all())
        results = True
    else:
        books = list(db.session.query(Book).order_by(Book.created_on.desc()).join(
            Reader).filter(Reader.private == False).all())
        results = False
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
                           books=current_group, page_numbers=page_numbers, results=results)
