from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL

from yacut import db
from yacut.models import URLMap


class URLMapForm(FlaskForm):
    """
    Creates an instance of the form that contains
    the original link, custom short link, and button fields.
    Checks the filling of the field with the original link,
    the correctness of the original url, the length of the
    user id for the short link.
    """
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

    def create_combined_url(self, short_id: str) -> URLMap:
        """
        Creates a combined link object based on the received
        data and returns it.
        """
        combined_url = URLMap(
            original=self.original_link.data,
            short=short_id
        )
        db.session.add(combined_url)
        db.session.commit()
        return combined_url
