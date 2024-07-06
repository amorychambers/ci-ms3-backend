"""
Test suite for all routes in the delete blueprint
"""
import flask.globals
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash


# class TestDeleteGenre(TestCase):
# """
# Testing methods for the route to delete a genre
# """

# @classmethod
# def setUpClass(cls) -> None:
#     """
#     Create new testuser in database to run tests on
#     """
#     testuser = Reader(username="testuser", password=generate_password_hash(
#         "testpass"), private=False)
#     db.session.add(testuser)
#     db.session.commit()
#     return super().setUpClass()

# def test_delete_genre(self, client):
#     """
#     Confirm that /delete_genre accepts a genre id, locations it in database, and deletes it
#     """
#     client.post(
#         "/sign_in", data={"username": "testuser", "password": "testpass"})
#     client.post(
#         "/add_genre", data={"genre_name": "testgenre", "genre_owner": flask.globals.session["user"]})
#     genre = db.session.query(Genre).filter(
#         Genre.genre_name == "testgenre").one()
#     response = client.get("/delete_genre/{}".format(genre.id))
#     # self.assertLocationHeader(response, "/my_library")
#     self.assertIsNone(db.session.query(Genre).filter(
#         Genre.id == genre.id).one_or_none())

# @classmethod
# def tearDownClass(cls) -> None:
#     """
#     Delete testuser from database
#     """
#     testuser = db.session.query(Reader).filter(
#         Reader.username == "testuser").one()
#     db.session.delete(testuser)
#     db.session.commit()
#     return super().tearDownClass()


class TestDeleteAccount(TestCase):
    """
    Testing methods for the route to delete a user's account from the database
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create new testuser in database to run tests on
        """
        testuser = Reader(username="testuser", password=generate_password_hash(
            "testpass"), private=False)
        db.session.add(testuser)
        db.session.commit()
        return super().setUpClass()
    

    def test_delete_account(self, client):
        """
        Confirm that /delete_account removes user and data from database
        """
        testuser = db.session.query(Reader).filter(Reader.username == "testuser").one_or_none()
        client.get("/delete_account/{}".format(testuser.id))
        self.assertNotIn("user", flask.globals.session)
        self.assertIsNone(db.session.query(Reader).filter(
            Reader.username == "testuser").one_or_none())
        
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete testuser from database
        """
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one_or_none()
        if testuser == None:
            return super().tearDownClass()
        else:
            db.session.delete(testuser)
            db.session.commit()
            return super().tearDownClass()