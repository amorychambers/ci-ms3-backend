"""
Test suite for all routes in the update blueprint
"""
import flask.globals
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash


class TestUpdateEntries(TestCase):
    """
    Testing methods for the route to update database entry for single book
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create new testuser and new testgenre in database to run tests on
        """
        testuser = Reader(username="testuser",
                          password=generate_password_hash("testpass"), private=False)
        genre = Genre(
            genre_name="testgenre", genre_owner="testuser")
        book = Book(
            book_title="testbook", author_name="testauthor", status="plan-to-read", favourite=False, review="", isbn=None, created_on="07/05/24 22:57:21", book_genre=203, book_owner="testuser"
        )
        db.session.add(testuser)
        db.session.add(genre)
        db.session.add(book)
        db.session.commit()
        return super().setUpClass()

    def test_edit_book(self, client):
        """
        Confirm that /edit_book route updates database entry
        """
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        testbook = db.session.query(Book).filter(
            Book.book_title == "testbook").one()
        client.post("/edit_book/{}".format(testbook.id), data={'status': 'complete', 'favourite': True, 'book_genre': 203,
                    'isbn': None, 'review': 'You know, now that I think about it, testauthor is not so bad'})
        updated_testbook = db.session.query(Book).filter(
            Book.id == testbook.id).one()
        self.assertEqual(updated_testbook.status, "complete")
        self.assertEqual(updated_testbook.favourite, True)
        self.assertIn("not so bad", updated_testbook.review)

    def test_edit_genre(self, client):
        """
        Confirm that /edit_genre route updates database entry
        """
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        genre = db.session.query(Genre).filter(
            Genre.genre_name == "testgenre", Genre.genre_owner == "testuser").one()
        client.post("/edit_genre/{}".format(genre.id), data={'genre_name': 'horror'})
        updated_genre = db.session.query(Genre).filter(Genre.id == genre.id).one()
        self.assertEqual(updated_genre.genre_name, "horror")

    def test_no_duplicate_genres(self, client):
        """
        Confirm that /edit_genre route does not update database entry if genre name already exists
        """
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        genre = db.session.query(Genre).filter(
            Genre.genre_owner == "testuser").one()
        # Following code snippet to test for flash messages on the page taken from suggestion of stackoverflow user Leo Skhrnkv, linked in readme credits
        response = client.post("/edit_genre/{}".format(genre.id), data={'genre_name': 'horror'}, follow_redirects=True)
        self.assertIn("That genre already exists in your library!", response.get_data(as_text=True))
        
    def test_edit_auth_fail(self, client):
        """
        Confirm that /edit_genre route does not update database entry when user not logged into session
        """
        genre = db.session.query(Genre).filter(
            Genre.genre_name == "testgenre", Genre.genre_owner == "testuser").one()
        client.post("/edit_genre/{}".format(genre.id), data={'genre_name': 'Horse Books'})
        updated_genre = db.session.query(Genre).filter(Genre.id == genre.id).one()
        self.assertNotEqual(updated_genre.genre_name, "Horse Books")


    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete testuser from database; cascade delete testgenre and testbook
        """
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()


class TestSaveBooks(TestCase):
    """
    Testing methods for the route to switch all books in a genre to the default misc
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create new testuser and new testgenre in database to run tests on
        """
        testuser = Reader(username="testuser",
                          password=generate_password_hash("testpass"), private=False)
        misc = Genre(
            genre_name="misc", genre_owner="testuser"
        )
        book = Book(
            book_title="testbook", author_name="testauthor", status="plan-to-read", favourite=False, review="", isbn=None, created_on="07/05/24 22:57:21", book_genre=261, book_owner="testuser"
        )
        db.session.add(testuser)
        db.session.add(misc)
        db.session.add(book)
        db.session.commit()
        return super().setUpClass()
    
    def test_save_book(self, client):
        """
        Confirm that /save_books changes genre to misc for all books in the genre passed to the route
        """
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        book = db.session.query(Book).filter(Book.book_title == "testbook").one()
        current_genre = db.session.query(Genre).filter(Genre.id == book.book_genre).one()
        self.assertEqual(book.book_genre, current_genre.id)
        client.post("/save_books/{}".format(current_genre.id))
        updated_book = db.session.query(Book).filter(Book.id == book.id).one()
        updated_genre = db.session.query(Genre).filter(Genre.genre_name == "misc", Genre.genre_owner == "testuser").one()
        self.assertEqual(updated_book.book_genre, updated_genre.id)
        


    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete testuser from database; cascade delete testgenre and testbook
        """
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()