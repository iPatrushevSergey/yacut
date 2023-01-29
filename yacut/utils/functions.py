from random import choices
from string import ascii_letters, digits

from yacut.models import URLMap


def get_unique_short_id(length: int) -> str:
    """
    The functions generates unique short_id. If these
    is a generated link in the database, it re-generates.
    """
    while True:
        short_id = ''.join(choices(ascii_letters + digits, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
