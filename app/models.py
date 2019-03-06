from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # the applications User model must inherit from UserMixin
from app import db, login


class User(UserMixin, db.Model):  # db.Model is the base class for SQLAlchemy; Multiple inheritance?
    # a user has many blog posts. 1-to-Many relationship
    id = db.Column(db.Integer, primary_key=True)  # primary key
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # apparently, this line places
    # an 'author' column in the Post table that will reference this table

    def __repr__(self):
        #  repr == representation. provides a representation of the model
        return f"<User {self.username}>"

    def set_password(self, password):  # upon registration
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  # upon login
        return check_password_hash(self.password_hash, password)


@login.user_loader  # this only loads a user session if client passes a session to the server
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    # many posts belong to one author. Many-to-1 relationship
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # index for sorting
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # similar to navigation property in EF

    def __repr__(self):
        return f"<Post {self.body}>"
