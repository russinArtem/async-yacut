from http import HTTPStatus
import re
import string

ALLOWED_CHARS = string.ascii_letters + string.digits
ALLOWED_SHORT_PATTERN = re.compile(f'^[{ALLOWED_CHARS}]+$')
RESERVED_SHORTS = {'files', 'redoc'}
MAX_ORIGINAL_LENGTH = 2048
MAX_SHORT_LENGTH = 16
SHORT_LENGTH = 6
MAX_SHORT_GENERATION_ATTEMPTS = 10
REDIRECT_ENDPOINT = 'redirect_view'
OPENAPI_DIR = '../'
LENGTH_ERROR = 'Количество символов не должно быть более {}'

# HTTP статусы
BAD_REQUEST = HTTPStatus.BAD_REQUEST
NOT_FOUND = HTTPStatus.NOT_FOUND
CREATED = HTTPStatus.CREATED
OK = HTTPStatus.OK
INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR
