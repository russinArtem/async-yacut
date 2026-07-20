from datetime import datetime
import random
import re

from flask import url_for

from . import db
from .constants import (
    ALLOWED_CHARS,
    ALLOWED_SHORT_PATTERN,
    INVALID_SHORT_ERROR,
    RESERVED_SHORT,
    SHORT_EXISTS_ERROR
)
from settings import Config

SHORT_GENERATION_ERROR = 'Не удалось сгенерировать уникальную короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(Config.MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(
        db.String(Config.MAX_SHORT_LENGTH), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_short():
        for _ in range(Config.MAX_SHORT_GENERATION_ATTEMPTS):
            short = ''.join(random.choices(
                ALLOWED_CHARS, k=Config.SHORT_LENGTH
            ))
            if not URLMap.query.filter_by(short=short).first():
                return short
        raise RuntimeError(SHORT_GENERATION_ERROR)

    @classmethod
    def create(cls, original, short=None):
        if short is None:
            short = ''
        short = short.strip()
        if short:
            if (
                len(short) > Config.MAX_SHORT_LENGTH
                or not re.match(ALLOWED_SHORT_PATTERN, short)
            ):
                raise ValueError(INVALID_SHORT_ERROR)
            if (
                short == RESERVED_SHORT
                or cls.query.filter_by(short=short).first()
            ):
                raise ValueError(SHORT_EXISTS_ERROR)
        else:
            short = cls.generate_short()
        url_map = cls(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @classmethod
    def get_by_short(cls, short):
        return cls.query.filter_by(short=short).first()

    def get_short_url(self):
        return url_for('redirect_view', short=self.short, _external=True)
