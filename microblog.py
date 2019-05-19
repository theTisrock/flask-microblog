from microblog_app import create_app, db
from microblog_app.models import User, Post

app = create_app()  # initialize app here


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}