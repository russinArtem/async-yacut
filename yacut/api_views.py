from flask import jsonify, request, send_from_directory

from . import app
from .constants import (
    CREATED,
    NOT_FOUND,
    OK,
    OPENAPI_DIR,
)
from .error_handlers import APIError
from .models import URLMap

EMPTY_BODY_ERROR = 'Отсутствует тело запроса'
URL_REQUIRED_ERROR = '"url" является обязательным полем!'
SHORT_NOT_FOUND_ERROR = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link_api():
    data = request.get_json(silent=True)
    if data is None:
        raise APIError(EMPTY_BODY_ERROR)
    if 'url' not in data:
        raise APIError(URL_REQUIRED_ERROR)
    url = data['url']
    try:
        url_map = URLMap.create(url, data.get('custom_id'), from_api=True)
    except Exception as error:
        raise APIError(str(error))
    return jsonify(
        {'url': url, 'short_link': url_map.get_short_url()}
    ), CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    if not (url_map := URLMap.get_by_short(short)):
        raise APIError(SHORT_NOT_FOUND_ERROR, NOT_FOUND)
    return jsonify({'url': url_map.original}), OK


@app.route('/redoc')
def openapi_spec():
    return send_from_directory(OPENAPI_DIR, 'openapi.yml')
