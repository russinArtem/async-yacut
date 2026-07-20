from flask import jsonify, render_template, request, send_from_directory

from . import app
from .constants import (
    BAD_REQUEST,
    CREATED,
    EMPTY_BODY_ERROR,
    INVALID_SHORT_ERROR,
    NOT_FOUND,
    OK,
    SHORT_EXISTS_ERROR,
    SHORT_NOT_FOUND_ERROR,
    URL_REQUIRED_ERROR,
)
from .error_handlers import APIError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link_api():
    data = request.get_json(silent=True)
    if data is None:
        raise APIError(EMPTY_BODY_ERROR, BAD_REQUEST)
    url = data.get('url')
    if not url:
        raise APIError(URL_REQUIRED_ERROR, BAD_REQUEST)
    try:
        url_map = URLMap.create(url, data.get('custom_id'))
    except ValueError as error:
        error_message = str(error)
        if error_message == INVALID_SHORT_ERROR:
            raise APIError(INVALID_SHORT_ERROR, BAD_REQUEST)
        elif error_message == SHORT_EXISTS_ERROR:
            raise APIError(SHORT_EXISTS_ERROR, BAD_REQUEST)
        else:
            raise APIError(error_message, BAD_REQUEST)
    return jsonify(
        {'url': url, 'short_link': url_map.get_short_url()}
    ), CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.get_by_short(short_id)
    if not url_map:
        raise APIError(SHORT_NOT_FOUND_ERROR, NOT_FOUND)
    return jsonify({'url': url_map.original}), OK


@app.route('/redoc/')
def redoc_view():
    return render_template('redoc.html')


@app.route('/redoc/openapi.yml')
def openapi_spec():
    return send_from_directory('../', 'openapi.yml')
