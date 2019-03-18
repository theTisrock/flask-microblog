from flask import Flask
from config import Config

app = Flask(__name__)  # using __name__ enables python to locate other files in this directory.

app.config.from_object(Config)

# the below line is non-conventional placement. This is because the above object "app" will be imported from
# this module into the routes module. Then, the decorators will add routes to the app object.
# then this module will import

from microblog_app import routes
