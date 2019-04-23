# errors

# When returning an error response, you can pass the error code along with it.
# return render_template(), [error_code]
from microblog_app import app, db
from flask import render_template
from flask_babel import _


@app.errorhandler(404)  # simple not found
def not_found_error(error):
    return render_template("http400.html", title=_("Not found")), 404


@app.errorhandler(500)  # internal: can occur for a number of resources. more complicated than simple 404
def internal_error(error):
    db.session.rollback()
    return render_template("http500.html", title=_("not found")), 500

# 500 error can happen at anytime.
# if in the middle of a database operation an error occurs, the current database session will be interrupted, meaning
# that transaction data integrity can be lost. If this occurs, we can use the rollback functionality to nullify
# the non-committed operation. If we do not do this, data can be modified in unexpected ways.
# ex, writing data when we should not OR the dbms may read bad data as a result of a "miss write".

# end errors
