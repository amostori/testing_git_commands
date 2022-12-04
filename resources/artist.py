import uuid

from flask import abort, request
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ArtistModel

blp = Blueprint('Artists', 'artists', 'Operations on artists')


@blp.route('/artist/<string:artist_id>')
class Artist(MethodView):
    def get(self, artist_id):
        artist = ArtistModel.query.get_or_404(artist_id)
        return artist

    def delete(self, artist_id):
        artist = ArtistModel.query.get_or_404(artist_id)
        db.session.delete(artist)
        db.session.commit()
        return {"message": "Item deleted."}


@blp.route('/artist')
class ArtistList(MethodView):
    def get(self):
        return ArtistModel.query.all()

    def post(self, artist_data):
        new_artist = ArtistModel(**artist_data)
        try:
            db.session.add(new_artist)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, 'An error occurred while inserting the item.')
        return new_artist
