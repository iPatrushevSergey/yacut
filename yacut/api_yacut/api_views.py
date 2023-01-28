from flask import jsonify, request, url_for

from yacut import app
from yacut.api_yacut.serializers import URLMapSerializer, is_data
from yacut.utils.error_handlers import InvalidAPIUsage
from yacut.web_yacut.models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    is_data(data)
    serializer = URLMapSerializer(data)
    serializer.validate()
    serializer.create_combined_url()
    data = {
        'url': serializer.original,
        'short_link': serializer.short,
    }
    return jsonify(data), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_url(short_id):
    short_url = url_for('url_clipping_view', _external=True) + short_id
    combined_url = URLMap.query.get(short_url)
    if combined_url is None:
        raise InvalidAPIUsage('Указанный ID не найден', 404)
    return jsonify(combined_url.to_dict()), 200
