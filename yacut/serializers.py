import re
from typing import Dict, Optional, Tuple

from yacut import db
from yacut.models import URLMap
from yacut.utils.error_handlers import InvalidAPIUsage
from yacut.utils.functions import get_unique_short_id


class URLMapSerializer:
    """
    Serializers the input data (validates data and creates
    a combined reference object). Processes the api post request
    to the create a combined link.
    """
    LENGTH_OF_SHORT_ID: int = 16

    def __new__(cls,
                *args: Tuple[Optional[Dict[str, str]]],
                **kwargs) -> 'URLMapSerializer':
        """
        Checks for input data before creating a serializer.
        """
        if args[0] is None:
            raise InvalidAPIUsage('Отсутствует тело запроса')
        return super().__new__(cls)

    def __init__(self, data: Optional[Dict[str, str]]) -> None:
        """
        Initializes the serializer with the transmitted data -
        a long original link and a custom short link.
        """
        self.original: str = data.get('url', 'no field')
        self.short: str = data.get('custom_id')

    def validate(self) -> None:
        """
        Runs all validating methods.
        """
        self.validate_url_field()
        self.validate_url_address()
        self.validate_short_id()
        self.validate_length_short_id()

    def validate_url_field(self) -> Optional[InvalidAPIUsage]:
        """
        Checks for the presence of a required url field.
        """
        if self.original == 'no field':
            raise InvalidAPIUsage('"url" является обязательным полем!')

    def validate_url_address(self) -> Optional[InvalidAPIUsage]:
        """
        Checks the correctness of the entered url (original link).
        """
        pattern = (
            r"^(https?:\/\/)?([\w.\-]+)\.([a-z]{2,6}\.?)(\/[\w.]*)*\/?$"
        )
        url_match = re.fullmatch(pattern, self.original)
        if not url_match:
            raise InvalidAPIUsage('Введён некорректный URL')

    def validate_short_id(self) -> Optional[InvalidAPIUsage]:
        """
        Checks for the presence of a short user link entered.
        If it is not there, then function of generating a unique
        link is started. Otherwise, the presence of the link
        in the database is checked. If the specified link is not
        occupied, then it is checked for the content of invalid
        characters.
        """
        if self.short is None or self.short == '':
            self.short = get_unique_short_id(6)
        elif URLMap.query.filter_by(short=self.short).first():
            raise InvalidAPIUsage(
                f'Имя "{self.short}" уже занято.'
            )
        else:
            pattern = r"[a-zA-Z0-9]+"
            short_id_match = re.fullmatch(pattern, self.short)
            if not short_id_match:
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )

    def validate_length_short_id(self) -> Optional[InvalidAPIUsage]:
        """
        Checks the entered short link for the allowed length
        (no more than 16 characters).
        """
        if len(self.short) > self.LENGTH_OF_SHORT_ID:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

    def create_combined_url(self) -> None:
        """
        Creates an instance of the class - a combined reference.
        """
        combined_url = URLMap(
            original=self.original,
            short=self.short
        )
        db.session.add(combined_url)
        db.session.commit()
