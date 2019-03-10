# This file is run at start up of the instance

from flask import Flask
from config import Config  # see Config class
from flask_sqlalchemy import SQLAlchemy  # Object Relational Mapper
from flask_migrate import Migrate  # Alembic migration extension for flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)  # read-in the configuration
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # makes sense. Migration links app code & DB.
# Similar to Code First versioning in ASP.NET Entity Framework
login = LoginManager(app)
login.login_view = "login"  # uses url_for underneath

from app import routes, models  # putting models at the bottom helps prevent circular dependencies
