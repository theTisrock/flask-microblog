from microblog_app import app, db  # entry point
from microblog_app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# end microblog
