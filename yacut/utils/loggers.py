import logging
from logging.handlers import RotatingFileHandler

from yacut.utils.constants import BASE_DIR, DT_FORMAT, ERROR_TEXT, LOG_FORMAT


def configure_logging(name):
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
        logging.exception(ERROR_TEXT, error)
        exit()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=10, encoding='utf-8'
    )
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DT_FORMAT)
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)
    logger.info('Приложение `yacut` запущено!')


api_logger = logging.getLogger('yacut.api_views')
view_logger = logging.getLogger('yacut.views')
commands_logger = logging.getLogger('yacut.utils.cli_commands')
