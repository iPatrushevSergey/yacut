from random import choices
from string import ascii_letters, digits

from flask import redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap


def get_unique_short_id(length):
    return ''.join(choices(ascii_letters + digits, k=length))


@app.route('/', methods=['GET', 'POST'])
def url_clipping_view():
    form = URLMapForm()
    if form.validate_on_submit():
        protocol_domain_suffix = url_for('url_clipping_view', _external=True)
        if not form.custom_id.data:
            path = get_unique_short_id(6)
        else:
            path = form.custom_id.data
        short_url = protocol_domain_suffix + path
        combined_url = URLMap(
            original=form.original_link.data,
            short=short_url
        )
        db.session.add(combined_url)
        db.session.commit()
        return redirect(url_for('url_clipping_view'))
    return render_template('cut.html', form=form)


@app.route('/<path:short>')
def redirect_view(short):
    url = URLMap.query.filter(short=short)
    return redirect(url.original)
