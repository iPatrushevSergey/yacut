from flask import flash, redirect, render_template, url_for

from yacut import app
from yacut.forms import URLMapForm
from yacut.functions import (get_combined_url,
                             get_unique_short_id)
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def url_clipping_view():
    form = URLMapForm()
    if form.validate_on_submit():
        domain = url_for('url_clipping_view', _external=True)
        path = form.custom_id.data
        if not path:
            path = get_unique_short_id(6, domain)
        elif URLMap.query.filter_by(short=domain + path).first():
            flash('Предложенный вариант короткой ссылки уже занят',
                  'not_unique')
            return render_template('cut.html', form=form)
        short_url = domain + path
        form.create_combined_url(short_url)
        flash(f'Ваша новая ссылка готова: {short_url}', 'done')
        return redirect(url_for('url_clipping_view'))
    return render_template('cut.html', form=form)


@app.route('/<path:short_id>/')
def redirect_view(short_id):
    return redirect(get_combined_url(short_id).original)
