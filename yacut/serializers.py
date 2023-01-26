from re import search

from flask import url_for

from yacut import db
from yacut.error_handlers import InvalidAPIUsage
from yacut.functions import get_unique_short_id
from yacut.models import URLMap


class URLMapSerializer:
    LENGTH_OF_SHORT_ID = 16

    def __init__(self, data):
        self.domain = url_for('url_clipping_view', _external=True)
        self.original = data.get('url')
        self.short = data.get('custom_id')

    def validate(self):
        self.validate_url_field()
        self.validate_url_address()
        self.validate_length_short_id()
        self.validate_short_id()

    def validate_url_field(self):
        if self.original is None:
            raise InvalidAPIUsage(
                'В запросе отсутсвует обязательное поле <url>'
            )

    def validate_url_address(self):
        pattern = (
            r"^[a-z]+://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        url_match = search(pattern, self.original)
        if not url_match:
            raise InvalidAPIUsage('Введён некорректный URL')

    def validate_length_short_id(self):
        if len(self.short) > self.LENGTH_OF_SHORT_ID:
            raise InvalidAPIUsage(
                'Длина поля `custom ID` не должна превышать 16 символов'
            )

    def validate_short_id(self):
        if self.short is None:
            self.short = self.domain + get_unique_short_id(6, self.domain)
        elif URLMap.query.filter_by(short=self.domain + self.short).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже занят'
            )
        else:
            self.short = self.domain + self.short

    def create_combined_url(self):
        combined_url = URLMap(
            original=self.original,
            short=self.short
        )
        db.session.add(combined_url)
        db.session.commit()
