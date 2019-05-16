# error_handlers

from microblog_app.errors import bp  # STEP B: import the Blueprint instance to apply handlers
from microblog_app import db
from flask import render_template
from flask_babel import _


@bp.errorhandler(404)
def not_found_error(error):
    return render_template("http400.html", title=_("Not found")), 404


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("http500.html", title=_("not found")), 500


# end error_handlers
