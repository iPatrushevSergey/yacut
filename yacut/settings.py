import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = ('"%(asctime)s - %(name)s:%(lineno)s - '
              '[%(levelname)s] - %(message)s"')
ERROR_TEXT = 'An error has occured: {}'


class Config(object):
    """
    Configures basic settings.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
