#  This class holds a config object that can be imported by the application.
#  It contains application configuration settings and is more maintainable through better
#  separation of concerns.

# Flask Mega Tutorial by Miguel Grinberg. Section 3, lecture 11

import os
# generate an abspath to dir containing db file
# __file__ resolves to this files location on disk when os.path() is used.
# adding .dirname(__file__) removes the filename from the path. The goal here is to get the directory
# of the file by using it as a target. Then we remove the filename and attach our own filename using
# os.path.join(dir, filename)
base_directory = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # to keep this secret, keep in an environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    # tell sqlalchemy the location of my SQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              "sqlite:///" + os.path.join(base_directory, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # used to signal application whenever an object changes.
    # If not set to false, will alert you every time you start the server. Annoying!
