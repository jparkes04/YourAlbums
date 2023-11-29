from app import db
from flask_login import UserMixin

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    trackname = db.Column(db.String(500))
    runtime = db.Column(db.Integer)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))


favourites_association_table = db.Table(
    "association_table",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("user.id")),
    db.Column("album_id", db.ForeignKey("album.id"))
)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500))
    password = db.Column(db.String(500))


class Album(db.Model):
    __tablename__ = "album"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    artist = db.Column(db.String(500))
    year = db.Column(db.Integer)
    tracks = db.relationship('Track', backref='album', lazy='dynamic')
