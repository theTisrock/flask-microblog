
# begin main __init__


# flask stuff
from flask import Blueprint
# extensions
# my stuff

bp = Blueprint("main", __name__)

from microblog_app.main import routes

# end main __init__
