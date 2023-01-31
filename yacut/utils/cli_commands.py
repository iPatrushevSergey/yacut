import csv
import sys

import click

from yacut import app, db
from yacut.models import URLMap
from yacut.settings import ERROR_TEXT
from yacut.utils.loggers import commands_logger


@app.cli.command('load-urls')
def load_urls_command() -> None:
    """
    The function of uploading url links
    to the database.
    """
    try:
        with open('yacut/utils/urls.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            counter = 0
            for row in reader:
                combined_url = URLMap(**row)
                db.session.add(combined_url)
                db.session.commit()
                counter += 1
        click.echo(f'Downloaded urls: {counter}')
        commands_logger.info(f'{counter} files uploaded successfully')
    except OSError as error:
        commands_logger.error(error)
        sys.exit(ERROR_TEXT.format(repr(error)))
    except csv.Error as error:
        commands_logger.error(error)
        sys.exit(ERROR_TEXT.format(repr(error)))
    except Exception as error:
        db.session.rollback()
        commands_logger.exception(error)
        sys.exit(ERROR_TEXT.format(repr(error)))
