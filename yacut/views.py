from flask import abort, flash, redirect, render_template, send_from_directory

from . import app
from .constants import NOT_FOUND, OPENAPI_DIR, REDIRECT_ENDPOINT
from .forms import FileForm, URLForm
from .models import URLMap
from .utils import upload_all_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.create(
                form.original_link.data, form.custom_id.data
            ).get_short_url()
        )
    except (ValueError, RuntimeError) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    try:
        download_links = upload_all_files(files)
    except Exception as error:
        flash(str(error))
        return render_template('files.html', form=form)
    uploaded_files = []
    try:
        for i, (file, download_link) in enumerate(
            zip(files, download_links)
        ):
            uploaded_files.append({
                'name': file.filename,
                'short_url': URLMap.create(
                    download_link,
                    commit=(i == len(files) - 1)
                ).get_short_url()
            })
    except (ValueError, RuntimeError) as error:
        flash(str(error))
        return render_template('files.html', form=form)
    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


@app.route('/<string:short>', endpoint=REDIRECT_ENDPOINT)
def redirect_view(short):
    if not (url_map := URLMap.get(short)):
        abort(NOT_FOUND)
    return redirect(url_map.original)


@app.route('/redoc')
def openapi_spec():
    return send_from_directory(OPENAPI_DIR, 'openapi.yml')
