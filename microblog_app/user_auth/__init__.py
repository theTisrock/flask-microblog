# begin user authentication package
from flask import Blueprint

bp = Blueprint("user_auth", __name__)

from microblog_app.user_auth import routes


# end user authentication package
