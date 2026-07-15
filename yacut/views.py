import asyncio

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import FileForm, URLForm
from .models import URLMap
from .utils import get_download_link, get_unique_short_id, upload_all_files

BASE_SHORT_URL = 'http://localhost/{}'


def create_short_link(original_link, custom_id):
    if not custom_id:
        short_id = get_unique_short_id()
    elif (
        custom_id == 'files'
        or URLMap.query.filter_by(short=custom_id).first()
    ):
        return None
    else:
        short_id = custom_id
    db.session.add(URLMap(original=original_link, short=short_id))
    db.session.commit()
    return BASE_SHORT_URL.format(short_id)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    short_link = None
    if form.validate_on_submit():
        short_link = create_short_link(
            form.original_link.data,
            form.custom_id.data.strip() if form.custom_id.data else ''
        )
        if short_link is None:
            flash('Предложенный вариант короткой ссылки уже существует.')
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileForm()
    uploaded_files = []
    if form.validate_on_submit():
        files = form.files.data
        locations = asyncio.run(upload_all_files(files))
        for i, file in enumerate(files):
            if (location := locations[i]):
                short_id = get_unique_short_id()
                db.session.add(URLMap(original=location, short=short_id))
                db.session.commit()
                uploaded_files.append({
                    'name': file.filename,
                    'short_link': BASE_SHORT_URL.format(short_id),
                    'download_link': asyncio.run(get_download_link(location))
                })
            else:
                uploaded_files.append({
                    'name': file.filename,
                    'short_link': None
                })
    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        abort(404)
    if url_map.original.startswith(('http://', 'https://')):
        return redirect(url_map.original)
    download_link = asyncio.run(get_download_link(url_map.original))
    if download_link:
        return redirect(download_link)
    abort(404)
