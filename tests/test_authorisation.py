import flask_unittest
import flask.globals
from libremate import create_app, db

# class TestDatabaseAuth(flask_unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         testuser = Reader(
#             username = "testuser",
#             password=generate_password_hash("jellyfish"),
#             private = True
#         )
#         db.session.add(testuser)
#         db.session.commit()

#     def test_sign_in(self):
#         self.assertTrue(db.session.query(Reader).filter(Reader.username == "testuser"))

#     @classmethod
#     def tearDownClass(cls):
#         testuser = db.session.query(Reader).filter(Reader.username == "testuser").one()
#         db.session.delete(testuser)
#         db.session.commit()

class TestAddBook(flask_unittest.ClientTestCase):
    app = create_app()

    def test_route(self, client):
        client.post("/sign_in", data={"username": "amory", "password": "sorryboss"})
        self.assertIn('user', flask.globals.session)