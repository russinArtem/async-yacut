from flask import abort, flash, redirect, render_template

from . import app
from .constants import NOT_FOUND
from .forms import FileForm, URLForm
from .models import URLMap
from .utils import upload_all_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(form.original_link.data, form.custom_id.data)
        short = url_map.get_short_url()
        return render_template('index.html', form=form, short=short)
    except ValueError as error:
        flash(str(error))
        return render_template('index.html', form=form)


def make_file_entry(file, download_link):
    filename = file.filename
    if not download_link:
        return {'name': filename, 'short': None}
    try:
        return {
            'name': filename,
            'short': URLMap.create(download_link).get_short_url()
        }
    except ValueError:
        return {'name': filename, 'short': None}


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    uploaded_files = [
        make_file_entry(file, download_link)
        for file, download_link in zip(files, upload_all_files(files))
    ]
    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


@app.route('/<string:short>', endpoint='redirect_view')
def redirect_view(short):
    url_map = URLMap.get_by_short(short)
    if not url_map:
        abort(NOT_FOUND)
    return redirect(url_map.original)
