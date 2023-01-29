import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config
from yacut.utils.loggers import configure_logging

configure_logging()
logging.info('Приложение `yacut` запущено!')
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import api_views, views
from yacut.utils import cli_commands, error_handlers
