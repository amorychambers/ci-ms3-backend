"""
Test suite for all routes in the settings blueprint
"""
import flask.globals
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader
from werkzeug.security import generate_password_hash


class TestPrivacy(TestCase):
    """
    Testing methods for the route to switch
    between a private and public account
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create new testuser in database to run tests on
        """
        testuser = Reader(username="testuser",
                          password=generate_password_hash(
                            "testpass"), private=True)
        db.session.add(testuser)
        db.session.commit()
        return super().setUpClass()

    def test_public_status(self, client):
        """
        Confirm that privacy accepts the passed
        status and switches between private and public
        """
        client.post(
            "/sign_in", data={"username": "testuser",
                              "password": "testpass"})
        client.post("/account/privacy/{}".format("public"))
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        self.assertFalse(testuser.private)

    def test_private_status(self, client):
        """
        Confirm that privacy accepts the passed
        status and switches between public and private
        """
        client.post(
            "/sign_in", data={"username": "testuser",
                              "password": "testpass"})
        client.post("/account/privacy/{}".format("private"))
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        self.assertTrue(testuser.private)

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
