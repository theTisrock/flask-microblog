# __init__
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging, os
from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

app = Flask(__name__)  # using __name__ enables python to locate other files in this directory.

# INSTANTIATIONS & CONFIGURATIONS: -------------------------------------------------

app.config.from_object(Config)  # load configurations

# database & migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# flask login
login = LoginManager(app)
login.login_view = 'login'

# flask mail
mail = Mail(app)

# flask bootstrap
bootstrap = Bootstrap(app)

# flask moment : Moment.js
moment = Moment(app)  # the JavaScript library must be added to the base template so moment.js will work

# flask babel
babel = Babel(app)

# if running in w/o debugger AKA if running in production
if not app.debug:

    # error notifications by email
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()  # why an empty tuple here???
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


# error log
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


# language support
@babel.localeselector  # extension
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])  # internal flask


from microblog_app import routes, models, errors

# end __init__
