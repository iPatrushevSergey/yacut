import logging
from logging.handlers import RotatingFileHandler

from yacut.utils.constants import BASE_DIR, DT_FORMAT, ERROR_TEXT, LOG_FORMAT


def configure_logging():
    try:
        log_dir = BASE_DIR / 'logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'yacut.log'
    except FileExistsError as error:
        logging.error(ERROR_TEXT, error)
        exit()
    except FileNotFoundError as error:
        logging.error(ERROR_TEXT, error)
        exit()
    except Exception as error:
        logging.error(ERROR_TEXT, error)
        exit()
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=10, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler,)
    )
