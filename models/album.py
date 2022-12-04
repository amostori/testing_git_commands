from db import db


class AlbumModel(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    artist = db.relationship('ArtistModel', back_populates='albums')
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), unique=False, nullable=False)
