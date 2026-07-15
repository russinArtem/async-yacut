import re

from flask import jsonify, request

from . import app
from .models import URLMap
from .views import create_short_link

ERROR_MESSAGES = {
    'empty_body': 'Отсутствует тело запроса',
    'invalid_short': 'Указано недопустимое имя для короткой ссылки',
    'url_required': '"url" является обязательным полем!',
    'short_exists': 'Предложенный вариант короткой ссылки уже существует.',
}


def error_response(message, status=400):
    return jsonify({'message': message}), status


@app.route('/api/id/', methods=['POST'])
def create_short_link_api():
    data = request.get_json(silent=True)
    if data is None:
        return error_response(ERROR_MESSAGES['empty_body'])
    url = data.get('url')
    if not url:
        return error_response(ERROR_MESSAGES['url_required'])
    custom_id = data.get('custom_id', '').strip()
    if len(custom_id) > 16:
        return error_response(ERROR_MESSAGES['invalid_short'])
    if custom_id and not re.match(r'^[a-zA-Z0-9]+$', custom_id):
        return error_response(ERROR_MESSAGES['invalid_short'])
    short_link = create_short_link(url, custom_id)
    if short_link is None:
        return error_response(ERROR_MESSAGES['short_exists'])
    return jsonify({'url': url, 'short_link': short_link}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({'message': 'Указанный id не найден'}), 404
    return jsonify({'url': url_map.original}), 200