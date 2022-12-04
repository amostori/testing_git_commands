from marshmallow import Schema, fields


class PlainAlbumSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)


class PlainArtistSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class PlainGenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class AlbumSchema(PlainAlbumSchema):
    artist_id = fields.Int(required=True, load_only=True)
    artist = fields.Nested(PlainArtistSchema(), dump_only=True)


class UpdatingAlbumSchema(Schema):
    album_id = fields.Int()
    artist = fields.Str()
    title = fields.Str()


class GenreSchema(PlainGenreSchema):
    artist_id = fields.Int(load_only=True)
    artist = fields.Nested(PlainArtistSchema(), dump_only=True)


class ArtistSchema(PlainArtistSchema):
    albums = fields.List(fields.Nested(PlainAlbumSchema()), dump_only=True)
    genres = fields.List(fields.Nested(PlainGenreSchema()), dump_only=True)


################################################################################

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
