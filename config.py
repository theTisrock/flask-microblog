import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

# configuration

# use environment variables to set/read sensitive information


class Config(object):
    # secret key environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    # tell sqlalchemy the location of my SQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              "sqlite:///" + os.path.join(basedir, "microblog.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # used to signal application whenever an object changes.
    # If not set to false, will alert you every time you start the server. Annoying!

    # email server environment variables
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['torok.chris@gmail.com']

    # translations
    LANGUAGES = ['en', 'es', 'de', 'hu']  # english, espanol, german, hungarian ... for babel
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')  # microsoft azure translations api key

    # sqlalchemy posts
    POSTS_PER_PAGE = 10

    # full text search
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # heroku
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


# end config
