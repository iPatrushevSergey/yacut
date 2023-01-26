from flask import jsonify, request

from yacut import app
from yacut.functions import get_combined_url
from yacut.serializers import URLMapSerializer


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    serializer = URLMapSerializer(data)
    serializer.validate()
    serializer.create_combined_url()
    data = {
        'short_link': serializer.short,
        'url': serializer.original,
    }
    return jsonify(data), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_url(short_id):
    return jsonify(get_combined_url(short_id).to_dict()), 200
