from flask import render_template, request, redirect, url_for, flash, session
from libremate import app, db
from libremate.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists
        q = db.session.query(Reader.id).filter(Reader.username==request.form.get("username").lower())
        if db.session.query(q.exists()).scalar():
            flash("Username already taken")
            redirect(url_for("register"))
        else:
            reader = Reader(
                username=request.form.get("username").lower(),
                password=generate_password_hash(request.form.get("new-password")),
                private=True if hasattr(request.form.get("private"), "checked") else False
            )
            db.session.add(reader)
            db.session.commit()
            session["user"] = request.form.get("username").lower()
            flash("Registration successful!")
            redirect(url_for("home"))
    
    return render_template("register.html")


