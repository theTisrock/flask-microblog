from datetime import datetime
from app import db


class User(db.Model):  # db.Model is the base class for SQLAlchemy
    # a user has many blog posts. 1-to-Many relationship
    id = db.Column(db.Integer, primary_key=True)  # primary key
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        #  repr == representation. provides a representation of the model
        return f"<User {self.username}>"


class Post(db.Model):
    # many posts belong to one author. Many-to-1 relationship
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # index for sorting
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # similar to navigation property in EF

    def __repr__(self):
        return f"<Post {self.body}"
