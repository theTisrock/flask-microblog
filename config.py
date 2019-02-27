#  This class holds a config object that can be imported by the application.
#  It contains application configuration settings and is more maintainable through better
#  separation of concerns.

# Flask Mega Tutorial by Miguel Grinberg. Section 3, lecture 11

import os

class Config(object):
    # to keep this secret, keep in an environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
