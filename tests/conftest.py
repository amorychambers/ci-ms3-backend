import flask_unittest
from libremate import create_app

class TestCase(flask_unittest.ClientTestCase):
    app = create_app()
    app.app_context().push()