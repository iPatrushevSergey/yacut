from flask import jsonify, request, url_for

from yacut import app
from yacut.models import URLMap
from yacut.serializers import URLMapSerializer
from yacut.utils.error_handlers import InvalidAPIUsage
from yacut.utils.loggers import api_logger


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    serializer = URLMapSerializer(data)
    serializer.validate()
    serializer.create_combined_url()
    domain = url_for('url_clipping_view', _external=True)
    data = {
        'url': serializer.original,
        'short_link': domain + serializer.short,
    }
    api_logger.info(f'Короткая ссылка `{serializer.short}` успешно создана')
    return jsonify(data), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    combined_url = URLMap.query.filter_by(short=short_id).first()
    if combined_url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(combined_url.to_dict()), 200
