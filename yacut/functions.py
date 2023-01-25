from random import choices
from string import ascii_letters, digits

from flask import url_for

from yacut.models import URLMap


def get_unique_short_id(length, domain):
    while True:
        path = ''.join(choices(ascii_letters + digits, k=length))
        if not URLMap.query.filter_by(short=domain + path).first():
            return path


def get_combined_url(short_id):
    short_url = url_for('url_clipping_view', _external=True) + short_id
    return URLMap.query.filter_by(short=short_url).first()
