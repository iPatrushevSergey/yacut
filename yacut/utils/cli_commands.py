import csv

import click

from yacut import app, db
from yacut.web_yacut.models import URLMap


@app.cli.command('load-urls')
def load_urls_command():
    """
    The function of uploading url links
    to the database.
    """
    with open('yacut/utils/urls.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            combined_url = URLMap(**row)
            db.session.add(combined_url)
            db.session.commit()
            counter += 1
    click.echo(f'Downloaded urls: {counter}')
