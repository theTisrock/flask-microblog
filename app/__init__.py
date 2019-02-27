# This file is run at start up of the instance

from flask import Flask
from config import Config  # see Config class

app = Flask(__name__)
app.config.from_object(Config)  # readin the configuration

from app import routes
