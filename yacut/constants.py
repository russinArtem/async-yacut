import re
from http import HTTPStatus

ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
ALLOWED_SHORT_PATTERN = re.compile(r'^[a-zA-Z0-9]+$')
MAX_SHORT_LENGTH = 16
BASE_SHORT_URL = 'http://localhost/{}'

# HTTP статусы
BAD_REQUEST = HTTPStatus.BAD_REQUEST
NOT_FOUND = HTTPStatus.NOT_FOUND
CREATED = HTTPStatus.CREATED
OK = HTTPStatus.OK
INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

# Тексты ошибок
EMPTY_BODY_ERROR = 'Отсутствует тело запроса'
URL_REQUIRED_ERROR = '"url" является обязательным полем!'
SHORT_EXISTS_ERROR = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_NOT_FOUND_ERROR = 'Указанный id не найден'
