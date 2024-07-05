import flask_unittest, flask.globals
from tests.conftest import TestCase
from libremate import create_app, db
from libremate.models.models import Reader


class TestNewUser(TestCase):

    def test_confirm_existing(self, client):
        self.assertTrue(db.session.query(Reader).filter(Reader.username == "amory").one_or_none())

    def test_create_user(self, client):
        response = client.post("/register", data={"username": "testuser", "new-password": "testpass", "private": False})
        self.assertTrue(db.session.query(Reader).filter(Reader.username == "testuser").one_or_none())
        self.assertIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/my_library")

    def test_existing_username(self, client):
        response = client.post("/register", data={"username": "amory", "new-password": "testpass", "private": False})
        self.assertNotIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/register")

    @classmethod
    def tearDownClass(cls) -> None:
        testuser = db.session.query(Reader).filter(Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()
    
