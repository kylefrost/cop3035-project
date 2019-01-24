from .. import db

class Word(db.Model):
    __tablename__ = "words"

    wordid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)

class Piece(db.Model):
    __tablename__ = "pieces"

    pieceid = db.Column(db.Integer, primary_key=True)
    side1 = db.Column(db.String)
    side2 = db.Column(db.String)
    side3 = db.Column(db.String)
    side4 = db.Column(db.String)
    side5 = db.Column(db.String)
    side6 = db.Column(db.String)
