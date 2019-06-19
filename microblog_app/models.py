
# begin models

# python
from datetime import datetime
from hashlib import md5
from time import time
import json
# flask
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
# extensions & packages
from flask_login import UserMixin
import jwt
# my stuff
from microblog_app import db, login
from microblog_app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append(ids[i], i)
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=Post.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# db signal handling for text search
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


# strong entity
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):  # UserMixin makes model compatible with flask-login
    id = db.Column(db.Integer, primary_key=True)  # flask login writes User.id to session
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_visited = db.Column(db.DateTime, default=datetime.utcnow())

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):  # used as representation of row data in the database used for each instance of a model
        return f"<user {self.username}>"

    def check_password(self, sanitized_password):  # upon login
        return check_password_hash(self.password_hash, sanitized_password)

    def pull_avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def set_password(self, sanitized_password):  # upon register
        self.password_hash = generate_password_hash(sanitized_password)

    def timestamp_on_request(self):  # time stamp to update last_visited in db upon request of any page
        self.last_visited = datetime.utcnow()
        # db.session.add(self)
        db.session.commit()

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)  # follow the target user
        # db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)
        return followed.union(self.posts).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},  # user id as payload
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            decoded_token_dict = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            id = decoded_token_dict['reset_password']
        except Exception as some_exception:
            return None
        return User.query.get(id)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']  # dunder field tells sqlalchemy not to add field to database
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # passing a function
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # uses relationship
    language = db.Column(db.String(5))  # five chars for language identification

    def __repr__(self):
        return f"<Post {self.body}, belongs to {self.user_id}>"

    @staticmethod
    def get_posts(filter_attr=None, filter_arg=None):
        posts = None
        if filter_attr is None:  # get all posts
            posts = Post.query.all()
        elif filter_attr == 'user_id':  # filter by username
            posts = Post.query.filter_by(user_id=filter_arg).all()
        elif filter_attr == 'timestamp':
            posts = Post.query.filter_by(timestamp=filter_arg).all()

        return posts


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

# end models
