"""
Test suite for all routes in the create blueprint
"""
import flask.globals
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash


class TestNewUser(TestCase):
    """
    Testing methods for the route to create a new user
    """

    def test_confirm_existing(self, client):
        self.assertTrue(db.session.query(Reader).filter(
            Reader.username == "amory").one_or_none())

    def test_create_user(self, client):
        """
        Confirm that the /register route creates a new user in the database,
        logs the user into session, and redirects to their library
        """
        response = client.post(
            "/register", data={"username": "testuser",
                               "new-password": "testpass", "private": False})
        self.assertTrue(db.session.query(Reader).filter(
            Reader.username == "testuser").one_or_none())
        self.assertIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/my_library")

    def test_existing_username(self, client):
        """
        Confirm that /register route will not create a duplicate
        username for one that already exists in database
        """
        response = client.post(
            "/register", data={"username": "amory",
                               "new-password": "testpass", "private": False})
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
    """
    Testing methods for the route to create a new genre
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create new testuser and new testgenre in database to run tests on
        """
        testuser = Reader(username="testuser",
                          password=generate_password_hash("testpass"),
                          private=False)
        existing_genre = Genre(
            genre_name="existing_genre", genre_owner="testuser")
        db.session.add(testuser)
        db.session.add(existing_genre)
        db.session.commit()
        return super().setUpClass()

    def test_new_genre(self, client):
        """
        Confirm /add_genre route creates a new genre in database
        for a logged in user and redirects to their library
        """
        client.post(
            "/sign_in", data={"username": "testuser",
                              "password": "testpass"})
        response = client.post(
            "/add_genre", data={"genre_name": "testgenre",
                                "genre_owner": flask.globals.session["user"]})
        self.assertLocationHeader(response, "/my_library")
        self.assertTrue(db.session.query(Genre).filter(
            Genre.genre_owner == "testuser",
            Genre.genre_name == "testgenre").one_or_none())

    def test_existing_genre(self, client):
        """
        Confirm /add_genre route will not create duplicate
        genres for the same user in the database
        """
        client.post(
            "/sign_in", data={"username": "testuser",
                              "password": "testpass"})
        response = client.post(
            "/add_genre", data={"genre_name": "existing_genre",
                                "genre_owner": flask.globals.session["user"]})
        self.assertLocationHeader(response, "/add_genre")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete testuser from database; cascade delete testgenre
        """
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()


class TestNewBook(TestCase):
    """
    Testing methods for the route to create a new book
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create new testuser and new testgenre in database to run tests on
        """
        testuser = Reader(username="testuser",
                          password=generate_password_hash("testpass"),
                          private=False)
        genre = Genre(
            genre_name="misc", genre_owner="testuser")
        db.session.add(testuser)
        db.session.add(genre)
        db.session.commit()
        return super().setUpClass()

    def test_new_book(self, client):
        """
        Confirm /add_book creates a new book entry
        in database and redirects to user's library
        """
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        response = client.post("/add_book", data={'book_title': 'testbook',
                                                  'author_name': 'testauthor',
                                                  'status': 'dropped',
                                                  'favourite': False,
                                                  'review':
                                                  'testauthor tests patience',
                                                  'isbn': None,
                                                  'created_on':
                                                  '07/05/24 22:57:21',
                                                  'book_genre': 1,
                                                  'book_owner': 'testuser'})
        self.assertLocationHeader(response, "/my_library")
        self.assertTrue(db.session.query(Book).filter(
            Book.book_owner == "testuser",
            Book.book_title == "testbook").one_or_none())

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete testuser from database; cascade delete testgenre
        """
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()
