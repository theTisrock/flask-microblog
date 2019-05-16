# begin errors
from flask import Blueprint

bp = Blueprint('errors', __name__)  # STEP A: now pass this to the "error_handlers" module

from microblog_app.errors import error_handlers  # STEP C: now import the handlers from here

# CONGRATULATIONS! You have avoided a circular dependency


# end __init__.py in errors directory
