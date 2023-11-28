from app import db


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    trackname = db.Column(db.String(500), index=True, unique=True)
    runtime = db.Column(db.Integer)
    value = db.Column(db.Float)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Favourite(db.Model):

class User(db.User):
    