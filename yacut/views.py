from flask import flash, redirect, render_template, url_for

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils.functions import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def url_clipping_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if short_id is None or short_id == '':
            short_id = get_unique_short_id(6)
        elif URLMap.query.filter_by(short=short_id).first():
            flash(f'Имя {short_id} уже занято!', 'not_unique')
            return render_template('cut.html', form=form)
        form.create_combined_url(short_id)
        short_url = url_for('url_clipping_view', _external=True) + short_id
        flash(f'Ваша новая ссылка готова: {short_url}', 'done')
        return redirect(url_for('url_clipping_view'))
    return render_template('cut.html', form=form)


@app.route('/<path:short_id>/')
def redirect_view(short_id):
    combined_url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(combined_url.original, code=302)
