from flask import redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def url_clipping_view():
    form = URLMapForm()
    if form.validate_on_submit():
        url = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('url_clipping_view'))
    return render_template('cut.html', form=form)
