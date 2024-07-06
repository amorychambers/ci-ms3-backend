import flask.globals
from tests.conftest import TestCase
from libremate import db
from libremate.models.models import Reader, Genre, Book
from werkzeug.security import generate_password_hash


class TestDeleteGenre(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        testuser = Reader(username="testuser", password=generate_password_hash(
            "testpass"), private=False)
        db.session.add(testuser)
        db.session.commit()
        return super().setUpClass()

    def test_delete_genre(self, client):
        client.post(
            "/sign_in", data={"username": "testuser", "password": "testpass"})
        client.post(
            "/add_genre", data={"genre_name": "testgenre", "genre_owner": flask.globals.session["user"]})
        genre = db.session.query(Genre).filter(Genre.genre_name == "testgenre").one()
        response = client.get("/delete_genre/{}".format(genre.id))
        # self.assertLocationHeader(response, "/my_library")
        self.assertIsNone(db.session.query(Genre).filter(Genre.id == genre.id).one_or_none())

    @classmethod
    def tearDownClass(cls) -> None:
        testuser = db.session.query(Reader).filter(
            Reader.username == "testuser").one()
        db.session.delete(testuser)
        db.session.commit()
        return super().tearDownClass()
