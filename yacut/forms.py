from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    ALLOWED_SHORT_PATTERN,
    LENGTH_ERROR,
    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH
)

ORIGINAL_LABEL = 'Длинная ссылка'
REQUIRED_FIELD_ERROR = 'Обязательное поле'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
SHORT_PATTERN_ERROR = 'Используйте только латиницу и цифры'
SUBMIT_CREATE_LABEL = 'Создать'
FILES_LABEL = 'Выберите файлы'
SUBMIT_UPLOAD_LABEL = 'Загрузить'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LABEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD_ERROR),
            Length(
                max=MAX_ORIGINAL_LENGTH,
                message=LENGTH_ERROR.format(MAX_ORIGINAL_LENGTH))
        ]
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=[
            Optional(),
            Length(
                max=MAX_SHORT_LENGTH,
                message=LENGTH_ERROR.format(MAX_SHORT_LENGTH)
            ),
            Regexp(
                ALLOWED_SHORT_PATTERN,
                message=SHORT_PATTERN_ERROR
            )
        ]
    )
    submit = SubmitField(SUBMIT_CREATE_LABEL)


class FileForm(FlaskForm):
    files = MultipleFileField(
        FILES_LABEL,
        validators=[DataRequired(message=REQUIRED_FIELD_ERROR)]
    )
    submit = SubmitField(SUBMIT_UPLOAD_LABEL)
