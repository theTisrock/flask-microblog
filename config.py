import os

# configuration

# use environment variables to set/read sensitive information


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
