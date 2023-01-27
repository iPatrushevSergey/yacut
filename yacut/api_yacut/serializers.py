from re import search

from flask import url_for

from yacut import db
from yacut.utils.error_handlers import InvalidAPIUsage
from yacut.utils.functions import get_unique_short_id
from yacut.web_yacut.models import URLMap


def is_data(data):
    if data is None:
        raise InvalidAPIUsage('Запрос не содержит каких-либо данных')


class URLMapSerializer:
    LENGTH_OF_SHORT_ID = 16

    def __init__(self, data):
        self.domain = url_for('url_clipping_view', _external=True)
        self.original = data.get('url', 'not found')
        self.short = data.get('custom_id', 'not found')

    def validate(self):
        self.validate_request_body()
        self.validate_url_field()
        self.validate_url_address()
        self.validate_length_short_id()
        self.validate_short_id()

    def validate_request_body(self):
        if self.original == 'not found' and self.short == 'not found':
            raise InvalidAPIUsage('Отсутсвует тело запроса')

    def validate_url_field(self):
        if self.original == 'not found':
            raise InvalidAPIUsage(
                'В запросе отсутсвует обязательное поле <url>'
            )

    def validate_url_address(self):
        pattern = (
            r"^(https?:\/\/)?([\w.\-]+)\.([a-z]{2,6}\.?)(\/[\w.]*)*\/?$"
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
