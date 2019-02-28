from app import db


class User(db.Model):  # db.Model is the base class for SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)  # primary key
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        #  repr == representation. provides a representation of the model
        return "<User {}>".format(self.username)
