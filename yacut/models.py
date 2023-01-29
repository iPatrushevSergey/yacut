from datetime import datetime
from typing import Dict

from yacut import db


class URLMap(db.Model):
    """
    The model for creating combined links contains the id
    fields, the original long link, the short custom link
    and the timestamp of the object creation.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict:
        """
        Converts an object field to a dictionary of the form:
        'url': 'original long link'.
        """
        return dict(
            url=self.original,
        )
