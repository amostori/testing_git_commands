from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import GenreModel, ArtistModel, AlbumGenre, AlbumModel
from schemas import GenreSchema, PlainGenreSchema

blp = Blueprint("Genres", "genres", description="Operations on genre")


@blp.route('/artist/<string:artist_id>/genre')
class GenreInArtist(MethodView):
    @blp.response(200, GenreSchema(many=True))
    def get(self, artist_id):
        artist = ArtistModel.query.get_or_404(artist_id)
        return artist.genres.all()

    @blp.arguments(GenreSchema)
    @blp.response(201, GenreSchema)
    def post(self, genre_data, artist_id):
        if GenreModel.query.filter(GenreModel.artist_id == artist_id).first():
            abort(400, message='This genre already exists.')
        genre = GenreModel(**genre_data, artist_id=artist_id)
        try:
            db.session.add(genre)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return genre


@blp.route('/genre/<string:genre_id>')
class Genre(MethodView):
    @blp.response(200, GenreSchema)
    def get(self, genre_id):
        genre = GenreModel.query.get_or_404(genre_id)
        return genre

    @blp.response(
        202,
        description="Deletes a genre if no album is tagged with it.",
        example={"message": "Genre deleted."},
    )
    @blp.alt_response(404, description="Genre not found.")
    @blp.alt_response(
        400,
        description="Returned if the Genre is assigned to one or more items. In this case, the Genre is not deleted.",
    )
    def delete(self, genre_id):
        genre = GenreModel.query.get_or_404(genre_id)

        if not genre.items:
            db.session.delete(genre)
            db.session.commit()
            return {"message": "Genre deleted."}
        abort(
            400,
            message="Could not delete Genre. Make sure Genre is not associated with any items, then try again.",
        )


@blp.route("/album/<string:album_id>/genre/<string:genre_id>")
class LinkGenresToAlbum(MethodView):
    @blp.response(201, GenreSchema)
    def post(self, album_id, genre_id):
        album = AlbumModel.query.get_or_404(album_id)
        genre = GenreModel.query.get_or_404(genre_id)

        album.genres.append(genre)

        try:
            db.session.add(album)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return genre

    @blp.response(200, GenreAlbumSchema)
    def delete(self, album_id, genre_id):
        album = AlbumModel.query.get_or_404(album_id)
        genre = GenreModel.query.get_or_404(genre_id)

        album.tags.remove(genre)

        try:
            db.session.add(album)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": album, "tag": genre}
