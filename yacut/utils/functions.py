from random import choices
from string import ascii_letters, digits

from yacut.web_yacut.models import URLMap


def get_unique_short_id(length, domain):
    while True:
        path = ''.join(choices(ascii_letters + digits, k=length))
        if not URLMap.query.filter_by(short=domain + path).first():
            return path
