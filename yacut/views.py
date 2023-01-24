from random import choices
from string import ascii_letters, digits

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap


def get_unique_short_id(length):
    return ''.join(choices(ascii_letters + digits, k=length))


@app.route('/', methods=['GET', 'POST'])
def url_clipping_view():
    form = URLMapForm()
    if form.validate_on_submit():
        domain = url_for('url_clipping_view', _external=True)
        if not form.custom_id.data:
            while True:
                path = get_unique_short_id(6)
                if not URLMap.query.filter_by(short=domain + path).first():
                    break
        else:
            path = form.custom_id.data
            if URLMap.query.filter_by(short=domain + path).first():
                flash('Предложенный вариант короткой ссылки уже занят', 'not_unique')
                return render_template('cut.html', form=form)
        short_url = domain + path
        combined_url = URLMap(
            original=form.original_link.data,
            short=short_url
        )
        db.session.add(combined_url)
        db.session.commit()
        flash(f'Ваша новая ссылка готова:  {short_url}', 'done')
        return redirect(url_for('url_clipping_view'))
    return render_template('cut.html', form=form)


@app.route('/<path:short>/')
def redirect_view(short):
    short_url = url_for('url_clipping_view', _external=True) + short
    url = URLMap.query.filter_by(short=short_url).first()
    return redirect(url.original)
