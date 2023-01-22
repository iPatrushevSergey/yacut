from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Enter the original long link',
        validators=[
            DataRequired(message='Required field'),
            URL(message='Invalid URL entered'),
        ],
    )
    custom_id = StringField(
        'Enter a short ID',
        validators=[
            Length(1, 16),
            Optional(),
        ],
    )
    submit = SubmitField('Add')
