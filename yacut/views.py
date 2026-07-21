from flask import abort, flash, redirect, render_template

from . import app
from .constants import NOT_FOUND, REDIRECT_ENDPOINT
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
    except Exception as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    uploaded_files = []
    try:
        for i, (file, download_link) in enumerate(
            zip(files, upload_all_files(files))
        ):
            try:
                uploaded_files.append({
                    'name': file.filename,
                    'short_url': URLMap.create(
                        download_link,
                        commit=(i == len(files) - 1)
                    ).get_short_url()
                })
            except Exception as error:
                flash(str(error))
                uploaded_files.append({
                    'name': file.filename,
                    'short_url': None
                })
    except Exception as error:
        flash(str(error))
        return render_template('files.html', form=form)
    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


@app.route('/<string:short>', endpoint=REDIRECT_ENDPOINT)
def redirect_view(short):
    if not (url_map := URLMap.get_by_short(short)):
        abort(NOT_FOUND)
    return redirect(url_map.original)
