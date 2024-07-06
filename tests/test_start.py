"""
Test suite fo the start blueprint
"""
import flask.globals
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader
from werkzeug.security import generate_password_hash


class TestGuestUser(TestCase):
    """
    Testing method for the redirection of home route
    """

    def test_no_session(self, client):
        """
        Confirm that a guest user who isn't signed into session is redirected to sign_in page
        """
        response = client.get("/")
        self.assertLocationHeader(response, "/sign_in")


class TestAuthorisedUser(TestCase):
    """
    Testing method for the redirection of home route
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create new testuser in database to run tests on
        """
        testuser = Reader(username="testuser", password=generate_password_hash(
            "testpass"), private=True)
        db.session.add(testuser)
        db.session.commit()
        return super().setUpClass()
    
    def test_session_user(self, client):
        """
        Confirm that a signed in user is redirected to their library
        """
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        response = client.get("/")
        self.assertLocationHeader(response, "/my_library")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete testuser from database
        """
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()