# This file is run at start up of the instance

from flask import Flask
from config import Config  # see Config class
from flask_sqlalchemy import SQLAlchemy  # Object Relational Mapper
from flask_migrate import Migrate  # Alembic migration extension for flask

app = Flask(__name__)
app.config.from_object(Config)  # read-in the configuration
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # makes sense. Migration links app code & DB.
# Similar to Code First versioning in ASP.NET Entity Framework

from app import routes, models
