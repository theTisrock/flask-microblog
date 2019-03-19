from datetime import datetime
from microblog_app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model): # UserMixin makes model compatible with flask-login
    id = db.Column(db.Integer, primary_key=True)  # flask login writes User.id to session
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):  # used as representation of row data in the database used for each instance of a model
        return f"<user {self.username}>"

    def set_password(self, sanitized_password):  # upon register
        self.password_hash = generate_password_hash(sanitized_password)

    def check_password(self, sanitized_password):  # upon login
        return check_password_hash(self.password_hash, sanitized_password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # passing a function
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # uses relationship

    def __repr__(self):
        return f"<Post {self.body}>"

# end models
