from http import HTTPStatus
import string

ALLOWED_CHARS = string.ascii_letters + string.digits
ALLOWED_SHORT_PATTERN = r'^[a-zA-Z0-9]+$'
RESERVED_SHORT = 'files'

# HTTP статусы
BAD_REQUEST = HTTPStatus.BAD_REQUEST
NOT_FOUND = HTTPStatus.NOT_FOUND
CREATED = HTTPStatus.CREATED
OK = HTTPStatus.OK
INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

# Тексты ошибок
EMPTY_BODY_ERROR = 'Отсутствует тело запроса'
URL_REQUIRED_ERROR = '"url" является обязательным полем!'
SHORT_NOT_FOUND_ERROR = 'Указанный id не найден'
INVALID_SHORT_ERROR = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS_ERROR = 'Предложенный вариант короткой ссылки уже существует.'
