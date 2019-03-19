import os
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration

# use environment variables to set/read sensitive information


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///" + os.path.join(basedir, 'microblog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# end config
