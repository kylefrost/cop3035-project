from .. import db

class Word(db.Model):
    __tablename__ = "words"

    wordid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
