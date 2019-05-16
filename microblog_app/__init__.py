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



# INSTANTIATIONS & CONFIGURATIONS: -------------------------------------------------


# database & migrations
db = SQLAlchemy()
migrate = Migrate()
# flask login
login = LoginManager()
login.login_view = 'login'
# flask mail
mail = Mail()
# flask bootstrap
bootstrap = Bootstrap()
# flask moment : Moment.js
moment = Moment()  # the JavaScript library must be added to the base template so moment.js will work
# flask babel
babel = Babel()


def create_app(config_class=Config):
    # instantiate application instance
    app = Flask(__name__)  # using __name__ enables python to locate other files in this directory.
    # load configurations
    app.config.from_object(Config)

    # initialize app w/ extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # connect/register blueprints with app
    from microblog_app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from microblog_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from microblog_app.user_auth import bp as user_auth_bp
    app.register_blueprint(user_auth_bp)

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
@babel.localeselector  # babel
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])  # flask


from microblog_app import routes, models, errors

# end __init__
