from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - %(name)s:%(lineno)s - [%(levelname)s] - %(message)s"'
ERROR_TEXT = 'An error has occured'
