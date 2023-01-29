import re

from flask import url_for

from yacut import db
from yacut.models import URLMap
from yacut.utils.error_handlers import InvalidAPIUsage
from yacut.utils.functions import get_unique_short_id


def is_data(data):
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')


class URLMapSerializer:
    LENGTH_OF_SHORT_ID = 16

    def __init__(self, data):
        self.original = data.get('url', 'no field')
        self.short = data.get('custom_id')

    def validate(self):
        self.validate_url_field()
        self.validate_url_address()
        self.validate_short_id()
        self.validate_length_short_id()

    def validate_url_field(self):
        if self.original == 'no field':
            raise InvalidAPIUsage('"url" является обязательным полем!')

    def validate_url_address(self):
        pattern = (
            r"^(https?:\/\/)?([\w.\-]+)\.([a-z]{2,6}\.?)(\/[\w.]*)*\/?$"
        )
        url_match = re.fullmatch(pattern, self.original)
        print(url_match)
        if not url_match:
            raise InvalidAPIUsage('Введён некорректный URL')

    def validate_short_id(self):
        if self.short is None or self.short == '':
            self.short = get_unique_short_id(6)
        elif URLMap.query.filter_by(short=self.short).first():
            raise InvalidAPIUsage(
                f'Имя "{self.short}" уже занято.'
            )
        else:
            pattern = r"[a-zA-Z0-9]+"
            short_id_match = re.fullmatch(pattern, self.short)
            print(short_id_match)
            if not short_id_match:
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    def validate_length_short_id(self):
        if len(self.short) > self.LENGTH_OF_SHORT_ID:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

    def create_combined_url(self):
        combined_url = URLMap(
            original=self.original,
            short=self.short
        )
        db.session.add(combined_url)
        db.session.commit()
