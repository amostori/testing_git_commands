from db import db


class GenreModel(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    artist_id = db.Column(db.Integer(), db.ForeignKey('artists.id'), nullable=False)
    artist = db.relationship('ArtistModel', back_populates='genres')
    albums = db.relationship("AlbumModel", back_populates="genres", secondary="album_genres")
