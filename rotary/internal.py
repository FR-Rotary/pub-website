from flask import Blueprint, render_template, redirect, request, url_for
from pycountry import countries

from rotary.db import get_db
from rotary.auth import login_required

bp = Blueprint('internal', __name__, url_prefix='/internal')


@bp.route('')
@login_required
def index():
    return render_template('internal/index.html')


@bp.route('/beers', methods=('GET', 'POST'))
@login_required
def beers():
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        style = request.form['style']
        country_code = request.form['country_code']
        abv = request.form['abv']
        volume = request.form['volume']
        price = request.form['price']
        category_id = request.form['category_id']
        available = 1 if request.form['available'] else 0

        print('DEBUG: available =', available)

        db.execute(
            'INSERT INTO beer '
            '(name, style, country_iso_3166_id, abv, '
            'volume_ml, price_kr, category_id, available) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (name, style, country_code, abv,
             volume, price, category_id, available)
        )

    beers = db.execute('SELECT * FROM beer ORDER BY name ASC')

    return render_template('internal/beers.html',
                           beers=beers, countries=countries)


@bp.route('/beers/delete/<int:n>', methods=('POST',))
@login_required
def delete_beer(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM beer WHERE id = ?', (n,))

    return redirect(url_for('internal.beers'))


@bp.route('/news', methods=('GET', 'POST'))
@login_required
def news():
    db = get_db()

    if request.method == 'POST':
        title_en = request.form['title_en']
        title_sv = request.form['title_sv']
        body_en = request.form['body_en']
        body_sv = request.form['body_sv']

        db.execute(
            'INSERT INTO news '
            '(time, title_en, title_sv, body_en, body_sv) '
            'VALUES (datetime(\'now\'), ?, ?, ?, ?)',
            (title_en, title_sv, body_en, body_sv)
        )

    posts = db.execute('SELECT * FROM news ORDER BY time DESC')

    return render_template('internal/news.html', posts=posts)


@bp.route('/news/delete/<int:n>', methods=('POST',))
@login_required
def delete_news_post(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM news WHERE id = ?', (n,))

    return redirect(url_for('internal.news'))


@bp.route('/workers', methods=('GET', 'POST'))
@login_required
def workers():
    db = get_db()

    if request.method == 'POST':
        display_name = request.form['display_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        telephone = request.form['telephone']
        email = request.form['email']
        address = request.form['address']
        note = request.form['note']
        status_id = request.form['status_id']

        db.execute(
            'INSERT INTO worker '
            '(display_name, first_name, last_name, '
            'telephone, email, address, note, status_id) '
            'VALUES (?¸ ?, ?¸ ?¸ ?, ?, ?, ?)',
            (display_name, first_name, last_name,
             telephone, email, address, note, status_id)
        )

    all_workers = db.execute('SELECT * FROM worker ORDER BY time DESC')

    return render_template('internal/workers.html', workers=all_workers)


@bp.route('/workers/delete/<int:n>', methods=('POST',))
@login_required
def delete_worker(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM worker WHERE id = ?', (n,))

    return redirect(url_for('internal.workers'))


@bp.route('/opening_hours', methods=('GET', 'POST'))
@login_required
def opening_hours():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date']
        start = request.form['start']
        end = request.form['end']

        # TODO: Mangle date
        print('DEBUG: Got date in opening_hours():', date)

        db.execute(
            'INSERT INTO opening_hours (date, start, end) VALUES (?, ?, ?)',
            (date, start, end)
        )

    all_hours = db.execute('SELECT * FROM opening_hours ORDER BY time DESC')

    return render_template('internal/opening_hours.html', opening_hours=all_hours)


@bp.route('/opening_hours/delete/<int:n>', methods=('POST',))
@login_required
def delete_opening_hours(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM opening_hours WHERE id = ?', (n,))

    return redirect(url_for('internal.opening_hours'))
