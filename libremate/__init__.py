import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


def create_app():
    from libremate.start.routes import start
    from libremate.authorisation.routes import authorisation
    from libremate.community.routes import community
    from libremate.create.routes import create
    from libremate.delete.routes import delete
    from libremate.library.routes import library
    from libremate.settings.routes import settings
    from libremate.update.routes import update

    app.register_blueprint(start)
    app.register_blueprint(authorisation)
    app.register_blueprint(community)
    app.register_blueprint(create)
    app.register_blueprint(delete)
    app.register_blueprint(library)
    app.register_blueprint(settings)
    app.register_blueprint(update)
    return app