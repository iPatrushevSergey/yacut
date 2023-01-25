from flask import jsonify, request

from yacut import app
from yacut.functions import get_combined_url


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    pass


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_url(short_id):
    return jsonify(get_combined_url(short_id).to_dict()), 200
