import os
from flask import Flask
from libremate.models.models import db
if os.path.exists("env.py"):
    import env


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    if os.environ.get("DEVELOPMENT") == "True":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
    else:
        uri = os.environ.get("DATABASE_URL")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

    db.init_app(app)

    from libremate.start.routes import start
    from libremate.authorisation.routes import authorisation
    from libremate.create.routes import create
    from libremate.delete.routes import delete
    from libremate.library.routes import library
    from libremate.settings.routes import settings
    from libremate.shared.routes import shared
    from libremate.update.routes import update

    app.register_blueprint(start)
    app.register_blueprint(authorisation)
    app.register_blueprint(shared)
    app.register_blueprint(create)
    app.register_blueprint(delete)
    app.register_blueprint(library)
    app.register_blueprint(settings)
    app.register_blueprint(update)

    return app
