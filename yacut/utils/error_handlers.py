from typing import Dict

from flask import jsonify, render_template
from flask.wrappers import Response
from werkzeug.exceptions import InternalServerError, NotFound

from yacut import app, db


class InvalidAPIUsage(Exception):
    """
    Initializes custom exceptions. Used
    in api_views responses.
    """
    status_code = 400

    def __init__(self, message: str, status_code: int = None) -> None:
        """
        Initializes an object with the properties
        message and status_code (default 400).
        """
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> Dict:
        """
        Returns a dictionary of the form:
        'message': 'error message'.
        """
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> Response:
    """
    Handles error objects that are created
    by the class InvalidAPIUsage.
    """
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error: NotFound) -> str:
    """
    Handles 404 web errors.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error: InternalServerError) -> str:
    """
    Handles 500 web errors.
    """
    db.session.rollback()
    return render_template('500.html'), 500
