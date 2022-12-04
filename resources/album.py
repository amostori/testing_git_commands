from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
import uuid

from models import AlbumModel
from schemas import AlbumSchema, UpdatingAlbumSchema, PlainAlbumSchema

blp = Blueprint('TestBlueprint', 'test_blueprint', 'Operations on test')


@blp.route('/album/<string:album_id>')
class Album(MethodView):
    @blp.response(200, AlbumSchema)
    def get(self, album_id):
        album = AlbumModel.query.get_or_404(album_id)
        return album

    @blp.arguments(UpdatingAlbumSchema)
    @blp.response(200, AlbumSchema)
    def put(self, album_data, album_id):
        album = AlbumModel.query.get_or_404(album_id)
        if album:
            album.title = album_data['title']
            album.artist = album_data['artist']
        else:
            album = AlbumModel(id=album_id, **album_data)
        db.session.add(album)
        db.session.commit()
        return album

    def delete(self, album_id):
        album = AlbumModel.query.get_or_404(album_id)
        db.session.delete(album)
        db.session.commit()
        return {"message": "Item deleted."}


@blp.route('/album')
class AlbumList(MethodView):
    @blp.response(200, AlbumSchema(many=True))
    def get(self):
        return AlbumModel.query.all()

    @blp.arguments(PlainAlbumSchema)
    @blp.response(201, AlbumSchema)
    def post(self, album_data):
        new_album = AlbumModel(**album_data)
        try:
            db.session.add(new_album)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occurred while inserting the item.')
        return new_album
