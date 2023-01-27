from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL

from yacut import db
from yacut.web_yacut.models import URLMap


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введён некорректный URL'),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Optional(),
        ],
    )
    submit = SubmitField('Создать')

    def create_combined_url(self, short_url):
        combined_url = URLMap(
            original=self.original_link.data,
            short=short_url
        )
        db.session.add(combined_url)
        db.session.commit()
