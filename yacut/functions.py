from random import choices
from string import ascii_letters, digits

from yacut import db
from yacut.models import URLMap


def get_unique_short_id(length, domain):
    while True:
        path = ''.join(choices(ascii_letters + digits, k=length))
        if not URLMap.query.filter_by(short=domain + path).first():
            return path


def create_combined_url(short_url, form):
    combined_url = URLMap(
        original=form.original_link.data,
        short=short_url
    )
    db.session.add(combined_url)
    db.session.commit()
