from flask import flash, redirect, render_template, url_for

from yacut import app
from yacut.utils.functions import get_unique_short_id
from yacut.web_yacut.forms import URLMapForm
from yacut.web_yacut.models import URLMap


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
    short_url = url_for('url_clipping_view', _external=True) + short_id
    combined_url = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(combined_url.original)
