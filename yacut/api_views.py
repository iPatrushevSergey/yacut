from typing import Dict, Optional, Union

from flask import jsonify, request, url_for
from flask.wrappers import Response

from yacut import app
from yacut.models import URLMap
from yacut.serializers import URLMapSerializer
from yacut.utils.error_handlers import InvalidAPIUsage
from yacut.utils.loggers import api_logger


@app.route('/api/id/', methods=['POST'])
def create_short_url() -> Response:
    """
    Processes requests to create a unique short link,
    performs data validation, saves the combined reference
    object and returns the fields of the created instance
    of the class (api requests).
    """
    data: Dict = request.get_json()
    serializer: URLMapSerializer = URLMapSerializer(data)
    serializer.validate()
    serializer.create_combined_url()
    domain: str = url_for('url_clipping_view', _external=True)
    data: Dict = {
        'url': serializer.original,
        'short_link': domain + serializer.short,
    }
    api_logger.info(f'Короткая ссылка `{serializer.short}` успешно создана')
    return jsonify(data), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id: str) -> Union[InvalidAPIUsage, Response]:
    """
    Taking a user unique short link, searches for the corresponding
    object and using a long link redirects to it (api requests).
    """
    combined_url: Optional[URLMap] = URLMap.query.filter_by(short=short_id).first()
    if combined_url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(combined_url.to_dict()), 200
