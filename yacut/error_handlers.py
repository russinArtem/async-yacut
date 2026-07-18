from flask import jsonify, render_template

from . import app, db
from .constants import NOT_FOUND, INTERNAL_SERVER_ERROR


class APIError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({'message': error.message}), error.status_code


@app.errorhandler(NOT_FOUND)
def page_not_found(error):
    return render_template('404.html'), NOT_FOUND


@app.errorhandler(INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), INTERNAL_SERVER_ERROR
