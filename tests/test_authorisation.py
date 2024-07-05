import flask.globals
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash, check_password_hash


class TestSignIn(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        testuser = Reader(username="testuser", password=generate_password_hash(
            "swordfish"), private=False)
        db.session.add(testuser)
        db.session.commit()
        return super().setUpClass()
    
    def test_sign_in(self, client):
        response = client.post("/sign_in", data={"username": "testuser", "password": "swordfish"})
        self.assertIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/my_library")

    def test_case_sensitive(self, client):
        response = client.post("/sign_in", data={"username": "testuser", "password": "sWoRdFiSh"})
        self.assertNotIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/sign_in")

    def test_wrong_password(self, client):
        response = client.post("/sign_in", data={"username": "testuser", "password": "horses?"})
        self.assertNotIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/sign_in")
    
    def test_wrong_username(self, client):
        response = client.post("/sign_in", data={"username": "unknownuser", "password": "swordfish"})
        self.assertNotIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/sign_in")

    def test_no_input(self, client):
        response = client.post("/sign_in", data={"username": "", "password": ""})
        self.assertNotIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/sign_in")
    
    @classmethod
    def tearDownClass(cls) -> None:
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()


class TestSignOut(TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        testuser = Reader(username="testuser", password=generate_password_hash(
            "swordfish"), private=False)
        db.session.add(testuser)
        db.session.commit()
        return super().setUpClass()
    
    def test_sign_out(self, client):
        client.post("/sign_in", data={"username": "testuser", "password": "swordfish"})
        response = client.get("/sign_out")
        self.assertNotIn("user", flask.globals.session)
        self.assertLocationHeader(response, "/")
    
    @classmethod
    def tearDownClass(cls) -> None:
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()