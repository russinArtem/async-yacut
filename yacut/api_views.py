from flask import abort, jsonify, render_template, request, send_from_directory

from . import app
from .constants import (
    BAD_REQUEST,
    BASE_SHORT_URL,
    CREATED,
    EMPTY_BODY_ERROR,
    NOT_FOUND,
    OK,
    SHORT_EXISTS_ERROR,
    SHORT_NOT_FOUND_ERROR,
    URL_REQUIRED_ERROR,
)
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link_api():
    data = request.get_json(silent=True)
    if data is None:
        abort(BAD_REQUEST, EMPTY_BODY_ERROR)
    url = data.get('url')
    if not url:
        abort(BAD_REQUEST, URL_REQUIRED_ERROR)
    try:
        url_map = URLMap.create(url, data.get('short'))
    except Exception:
        abort(BAD_REQUEST, SHORT_EXISTS_ERROR)
    return jsonify(
        {'url': url, 'short': BASE_SHORT_URL.format(url_map.short)}
    ), CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short):
    url_map = URLMap.get_by_short(short)
    if not url_map:
        abort(NOT_FOUND, SHORT_NOT_FOUND_ERROR)
    return jsonify({'url': url_map.original}), OK


@app.route('/redoc/')
def redoc_view():
    return render_template('redoc.html')


@app.route('/redoc/openapi.yml')
def openapi_spec():
    return send_from_directory('../', 'openapi.yml')
