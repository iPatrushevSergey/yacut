import logging
import sys
from logging.handlers import RotatingFileHandler

from yacut.settings import BASE_DIR, DT_FORMAT, ERROR_TEXT, LOG_FORMAT


def configure_logging(name: str) -> None:
    """
    Configures the root logger (the place where logs are saved,
    logging level, handler, formatter).
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(LOG_FORMAT, DT_FORMAT)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    try:
        log_dir = BASE_DIR / 'logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'yacut.log'
    except FileExistsError as error:
        logger.error(ERROR_TEXT.format(repr(error)))
        sys.exit(ERROR_TEXT.format(repr(error)))
    except FileNotFoundError as error:
        logger.error(ERROR_TEXT.format(repr(error)))
        sys.exit(ERROR_TEXT.format(repr(error)))
    except Exception as error:
        logger.exception(ERROR_TEXT.format(repr(error)))
        sys.exit(ERROR_TEXT.format(repr(error)))
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=10, encoding='utf-8'
    )
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)
    logger.info('Приложение `yacut` запущено!')


# Creating modular handlers.
api_logger = logging.getLogger('yacut.api_views')
commands_logger = logging.getLogger('yacut.utils.cli_commands')
serializer_logger = logging.getLogger('yacut.serializers')
view_logger = logging.getLogger('yacut.views')
