from typing import Dict

from flask import flash, redirect, render_template
from werkzeug.wrappers.response import Response

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils.functions import get_unique_short_id
from yacut.utils.loggers import view_logger


@app.route('/', methods=['GET', 'POST'])
def url_clipping_view() -> str:
    """
    Creates an instance of the form and sends it to the user
    (get request). Also validates the form with data sent
    by the user with a post request. If there is no user link,
    a short link is automatically generated. Next, a combined
    link object is created. A notification is sent to the user
    with his created short link (web requests).
    """
    form = URLMapForm()
    if form.validate_on_submit():
        short_id: str = form.custom_id.data
        if short_id is None or short_id == '':
            short_id: str = get_unique_short_id(6)
        elif URLMap.query.filter_by(short=short_id).first():
            flash(f'Имя {short_id} уже занято!', 'not_unique')
            return render_template('cut.html', form=form)
        combined_url: URLMap = form.create_combined_url(short_id)
        flash('Ваша новая ссылка готова:', 'done')
        context: Dict = {
            'form': form,
            'combined_url': combined_url
        }
        view_logger.info(f'Короткая ссылка `{short_id}` успешно создана')
        return render_template('cut.html', **context)
    return render_template('cut.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id) -> Response:
    """
    Taking a user unique short link, searches for the corresponding
    object and using a long link redirects to it (web requests).
    """
    combined_url: URLMap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(combined_url.original)
