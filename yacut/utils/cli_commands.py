import csv
import logging

import click

from yacut import app, db
from yacut.models import URLMap
from yacut.utils.constants import ERROR_TEXT


@app.cli.command('load-urls')
def load_urls_command():
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
    except OSError as error:
        logging.error(ERROR_TEXT, error)
        exit()
    except csv.Error as error:
        logging.error(ERROR_TEXT, error)
        exit()
    except Exception as error:
        logging.error(ERROR_TEXT, error)
        exit()
