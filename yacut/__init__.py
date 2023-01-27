from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut.utils import error_handlers
from yacut.web_yacut import views
from yacut.api_yacut import api_views
