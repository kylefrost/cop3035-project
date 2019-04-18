from .. import db

# SQL Alchemy class for getting words from database
class Word(db.Model):
    __tablename__ = "words"

    wordid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
