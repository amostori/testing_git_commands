from db import db


class ArtistModel(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    albums = db.relationship('AlbumModel', back_populates='artist', lazy='dynamic')
    genres = db.relationship('GenreModel', back_populates='artist', lazy='dynamic')
