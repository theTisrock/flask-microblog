from app import app  # this is where flask obtains the application instance

# customize the shell context to include common imports
from app import db
from app.models import User, Post


@app.shell_context_processor  # for using command-line, preloaded flask environment w/ imports
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}
