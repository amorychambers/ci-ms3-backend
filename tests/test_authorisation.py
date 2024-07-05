import unittest
from flask import session
from libremate import db
from libremate.models.models import Reader
from werkzeug.security import generate_password_hash, check_password_hash
from libremate.authorisation.routes import sign_in, sign_out


class TestSecurity(unittest.TestCase):

    def setUp(self):
        self.password = generate_password_hash(
            "sharkfish", method='pbkdf2:sha1', salt_length=8)

    def test_correct_password(self):
        self.assertTrue(check_password_hash(
            self.password, "sharkfish"), "Correct password does not match")

    def test_incorrect_password(self):
        self.assertFalse(check_password_hash(
            self.password, "purplepepperminthorse"), "Incorrect password flagged correct")

    def test_case_sensitivity(self):
        self.assertFalse(check_password_hash(
            self.password, "sHaRkfIsH"), "Password is not case sensitive")
        

class TestDatabaseAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        testuser = Reader(
            username = "testuser",
            password=generate_password_hash("jellyfish"),
            private = True
        )
        db.session.add(testuser)
        db.session.commit()

    def test_sign_in(self):
        self.assertTrue(db.session.query(Reader).filter(Reader.username == "testuser"))

    @classmethod
    def tearDownClass(cls):
        testuser = db.session.query(Reader).filter(Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()