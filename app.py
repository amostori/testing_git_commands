from flask import Flask
from resources.album import blp as AlbumBlueprint
from resources.artist import blp as ArtistBlueprint
from resources.genre import blp as GenreBlueprint
from flask_smorest import Api
import os
from db import db
import models


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Tutorial1 REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)
    with app.app_context():
        db.create_all()
    api.register_blueprint(AlbumBlueprint)
    api.register_blueprint(ArtistBlueprint)
    api.register_blueprint(GenreBlueprint)
    return app
