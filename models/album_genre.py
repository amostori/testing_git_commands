from db import db


class AlbumGenre(db.Model):
    __tablename__ = "album_genres"

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
