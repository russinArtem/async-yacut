from datetime import datetime
import random
import re

from flask import url_for

from . import db
from .constants import (
    ALLOWED_CHARS,
    ALLOWED_SHORT_PATTERN,
    LENGTH_ERROR,
    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_GENERATION_ATTEMPTS,
    MAX_SHORT_LENGTH,
    REDIRECT_ENDPOINT,
    RESERVED_SHORTS,
    SHORT_LENGTH
)

INVALID_SHORT_ERROR = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS_ERROR = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_GENERATION_ERROR = f'Провал. Попыток - {MAX_SHORT_GENERATION_ATTEMPTS}'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_short():
        for _ in range(MAX_SHORT_GENERATION_ATTEMPTS):
            short = ''.join(random.choices(
                ALLOWED_CHARS, k=SHORT_LENGTH
            ))
            if (
                short not in RESERVED_SHORTS
                and URLMap.get(short) is None
            ):
                return short
        raise RuntimeError(SHORT_GENERATION_ERROR)

    @staticmethod
    def create(original, short=None, validate=False, commit=True):
        if validate and len(original) > MAX_ORIGINAL_LENGTH:
            raise ValueError(LENGTH_ERROR.format(MAX_ORIGINAL_LENGTH))
        if short:
            if validate and (
                len(short) > MAX_SHORT_LENGTH
                or not re.match(ALLOWED_SHORT_PATTERN, short)
            ):
                raise ValueError(INVALID_SHORT_ERROR)
            if short in RESERVED_SHORTS or URLMap.get(short):
                raise ValueError(SHORT_EXISTS_ERROR)
        url_map = URLMap(
            original=original,
            short=short or URLMap.generate_short()
        )
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        return url_for(REDIRECT_ENDPOINT, short=self.short, _external=True)
