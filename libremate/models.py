from libremate import db


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    books = db.relationship("Book", backref="reader", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.username


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(20), nullable=False)
    genre_owner = db.Column(db.String(15), db.ForeignKey(
        "reader.username"), nullable=False)
    books = db.relationship("Book", backref="genre", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.genre_name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String, nullable=False)
    favourite = db.Column(db.Boolean, nullable=False)
    review = db.Column(db.Text)
    isbn = db.Column(db.String)
    created_on = db.Column(db.Date, nullable=False)
    book_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))
    book_owner = db.Column(db.String(15), db.ForeignKey(
        "reader.username"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return f"{self.book_title} - {self.author_name}"
