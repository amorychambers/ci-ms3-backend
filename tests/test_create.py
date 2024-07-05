import flask.globals, datetime
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash


class TestNewUser(TestCase):

    def test_confirm_existing(self, client):
        self.assertTrue(db.session.query(Reader).filter(
            Reader.username == "amory").one_or_none())

    def test_create_user(self, client):
        response = client.post(
            "/register", data={"username": "testuser", "new-password": "testpass", "private": False})
        self.assertTrue(db.session.query(Reader).filter(
            Reader.username == "testuser").one_or_none())
        self.assertIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/my_library")

    def test_existing_username(self, client):
        response = client.post(
            "/register", data={"username": "amory", "new-password": "testpass", "private": False})
        self.assertNotIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/register")

    @classmethod
    def tearDownClass(cls) -> None:
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()


class TestNewGenre(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        testuser = Reader(username="testuser",
                          password=generate_password_hash("testpass"), private=False)
        existing_genre = Genre(
            genre_name="existing_genre", genre_owner="testuser")
        db.session.add(testuser)
        db.session.add(existing_genre)
        db.session.commit()
        return super().setUpClass()

    def test_new_genre(self, client):
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        response = client.post(
            "/add_genre", data={"genre_name": "testgenre", "genre_owner": flask.globals.session["user"]})
        self.assertLocationHeader(response, "/my_library")
        self.assertTrue(db.session.query(Genre).filter(
            Genre.genre_owner == "testuser", Genre.genre_name == "testgenre").one_or_none())

    def test_existing_genre(self, client):
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        response = client.post(
            "/add_genre", data={"genre_name": "existing_genre", "genre_owner": flask.globals.session["user"]})
        self.assertLocationHeader(response, "/add_genre")

    @classmethod
    def tearDownClass(cls) -> None:
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()


class TestNewBook(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        testuser = Reader(username="testuser",
                          password=generate_password_hash("testpass"), private=False)
        genre = Genre(
            genre_name="misc", genre_owner="testuser")
        db.session.add(testuser)
        db.session.add(genre)
        db.session.commit()
        return super().setUpClass()

    def test_new_book(self, client):
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        response = client.post("/add_book", data={'book_title': 'testbook', 'author_name': 'testauthor', 'status': 'dropped', 'favourite': False, 'review': 'This book sucks ass. Who the hell does this testauthor guy think he is?', 'isbn': None, 'created_on': '07/05/24 22:57:21', 'book_genre': 5, 'book_owner': 'testuser'})
        self.assertLocationHeader(response, "/my_library")
        self.assertTrue(db.session.query(Book).filter(Book.book_owner == "testuser", Book.book_title == "testbook").one_or_none())

    @classmethod
    def tearDownClass(cls) -> None:
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()
