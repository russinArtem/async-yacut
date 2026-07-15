from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=16, message='Длина не более 16 символов'),
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message='Используйте только латиницу и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[DataRequired(message='Выберите файлы')]
    )
    submit = SubmitField('Загрузить')
