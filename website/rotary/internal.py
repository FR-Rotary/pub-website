from flask import Blueprint, render_template, redirect, request, url_for, g, Response
from flask.globals import current_app
from pycountry import countries
from tempfile import TemporaryDirectory
import subprocess
import os
import datetime

from rotary.db import get_db
from rotary.auth import login_required
from rotary.i18n import strings_en
from rotary.util import dict_from_row

bp = Blueprint('internal', __name__, url_prefix='/internal')


@bp.route('')
@login_required
def index():
    return render_template('internal/index.html')


@bp.route('/')
@login_required
def index_slash_redirect():
    return redirect(url_for('internal.index'))


@bp.route('/beers', methods=('GET', 'POST'))
@login_required
def beers():
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        style = request.form['style']
        country_code = int(request.form['country_code'])
        abv = float(request.form['abv'].replace(',', '.'))
        volume = int(request.form['volume'])
        price = int(request.form['price'])
        category_id = int(request.form['category_id'])
        available = 1 if request.form.get('available') else 0

        print('DEBUG: available =', available)

        db.execute(
            'INSERT INTO beer '
            '(name, style, country_iso_3166_id, abv, '
            'volume_ml, price_kr, category_id, available) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (name, style, country_code, abv,
             volume, price, category_id, available)
        )
        db.commit()

    beers = db.execute(
        'SELECT available, beer.name, '
        'IFNULL(beer_category.name, \'<unknown category>\') as category, '
        'beer.id, style, abv, country_iso_3166_id, volume_ml, price_kr '
        'FROM beer LEFT OUTER JOIN beer_category '
        'ON beer.category_id = beer_category.id '
        'ORDER BY beer.name ASC'
    )
    categories = db.execute(
        'SELECT * FROM beer_category ORDER BY id ASC').fetchall()

    return render_template(
        'internal/beers.html',
        beers=beers,
        countries=countries,
        categories=categories,
        category_names=strings_en['menu']['beer_categories']
    )

@bp.route('/beers/edit/<int:n>', methods=('GET', 'POST'))
@login_required
def edit_beer(n):
    if request.method == 'POST' and n is not None:
        db = get_db()

        name = request.form['name']
        style = request.form['style']
        country_code = int(request.form['country_code'])
        abv = float(request.form['abv'].replace(',', '.'))
        volume = int(request.form['volume'])
        price = int(request.form['price'])
        category_id = int(request.form['category_id'])
        available = 1 if request.form.get('available') else 0

        db.execute(
            'UPDATE beer  SET '
            'name = ?, style = ?, country_iso_3166_id = ?, abv = ?, '
            'volume_ml = ?, price_kr = ?, category_id = ?, available = ? '
            'WHERE id = ?'
            ,
            (name, style, country_code, abv,
             volume, price, category_id, available, n)
        )

        db.commit()
        return redirect(url_for('internal.beers'))

    if n is not None:
        db = get_db()
        beer = db.execute('SELECT * FROM beer WHERE beer.id = ? ', (n,)).fetchone()
        categories = db.execute(
            'SELECT * FROM beer_category ORDER BY id ASC').fetchall()

        return render_template(
                'internal/edit_beer.html',
                beer = beer,
                countries=countries,
                categories=categories,
                category_names=strings_en['menu']['beer_categories']
                )

    return redirect(url_for('internal.beers'))


@bp.post('/beers/delete/<int:n>')
@login_required
def delete_beer(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM beer WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.beers'))

@bp.post('/beers/toggle/<int:n>')
@login_required
def toggle_beer(n):
    if n is not None:
        db = get_db()
        db.execute('UPDATE beer SET available = NOT available WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.beers'))

@bp.get('/food')
@login_required
def food():
    db = get_db()
    foods = db.execute('SELECT * FROM food ORDER BY name ASC').fetchall()
    snacks = db.execute('SELECT * FROM snack ORDER BY name ASC').fetchall()

    return render_template('internal/food.html', foods=foods, snacks=snacks)

@bp.post('/food/add')
@login_required
def add_food():
    db = get_db()
    name = request.form['name']
    price = request.form['price']
    db.execute( 'INSERT INTO food (name, price_kr) VALUES (?,?)', (name, price))
    db.commit()

    return redirect(url_for('internal.food'))


@bp.post('/food/delete/<int:n>')
@login_required
def delete_food(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM food WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.food'))

@bp.post('/snacks/add')
@login_required
def add_snacks():
    db = get_db()
    name = request.form['name']
    price = request.form['price']
    db.execute( 'INSERT INTO snack (name, price_kr) VALUES (?,?)', (name, price))
    db.commit()

    return redirect(url_for('internal.food'))


@bp.post('/snacks/delete/<int:n>')
@login_required
def delete_snacks(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM snack WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.food'))


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
        db.commit()

    posts = db.execute('SELECT * FROM news ORDER BY time DESC')
    #posts = list(posts)

    return render_template('internal/news.html', posts=posts)


@bp.post('/news/delete/<int:n>')
@login_required
def delete_news_post(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM news WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.news'))


@bp.route('/workers', methods=('GET', 'POST'))
@login_required
def workers():

    db = get_db()
    all_workers = db.execute('SELECT * FROM worker ORDER BY display_name ASC')
    worker_status = db.execute('SELECT * FROM worker_status').fetchall()

    return render_template('internal/workers.html', workers=all_workers, worker_status=worker_status)


@bp.route('/workers/add', methods=('POST', 'GET'))
@login_required
def add_workers():
    # TODO: Mailing list stuff
    db = get_db()
    worker_status = db.execute('SELECT * FROM worker_status').fetchall()

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
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (display_name, first_name, last_name,
             telephone, email, address, note, status_id)
        )
        db.commit()

        return redirect(url_for('internal.workers'))

    return render_template('internal/add_workers.html', worker=None, worker_status=worker_status)


@bp.route('/workers/edit/<int:n>', methods=('POST', 'GET'))
@login_required
def edit_worker(n):
    # TODO: Mailing list stuff
    db = get_db()
    worker_status = db.execute('SELECT * FROM worker_status').fetchall()

    if request.method == 'GET' and n is not None:
        worker = db.execute(
            'SELECT * FROM worker WHERE id = ?',
            (n,)
        ).fetchone()

        if worker is None:
            return redirect(url_for('internal.add_workers'))

        return render_template('internal/add_workers.html', worker=worker, worker_status=worker_status)
    elif request.method == 'POST' and n is not None:
        display_name = request.form['display_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        telephone = request.form['telephone']
        email = request.form['email']
        address = request.form['address']
        note = request.form['note']
        status_id = request.form['status_id']

        db.execute(
            'UPDATE worker SET '
            'display_name = ?, first_name = ?, last_name = ?, telephone = ?, '
            'email = ?, address = ?, note = ?, status_id = ? '
            'WHERE id = ?',
            (display_name, first_name, last_name, telephone, email, address,
             note, status_id, n)
        )
        db.commit()

    return redirect(url_for('internal.workers'))


@bp.route('/workers/delete/<int:n>', methods=('POST', 'GET'))
@login_required
def delete_worker(n):
    # TODO: Mailing list stuff
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM worker WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.workers'))


@bp.route('/opening_hours', methods=('GET', 'POST'))
@login_required
def opening_hours():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date']
        start = request.form['start']
        end = request.form['end']

        # Check if we already have an entry for the given date
        existing_entry = db.execute(
            'SELECT id FROM opening_hours WHERE date = date(?)', (date,)
        ).fetchone()

        if existing_entry:
            db.execute(
                'UPDATE opening_hours SET start = time(?), end = time(?) '
                'WHERE id = ?',
                (start, end, existing_entry['id'])
            )
        else:  # TODO: Mangle date
            db.execute(
                'INSERT INTO opening_hours (date, start, end) '
                'VALUES (date(?), time(?), time(?))',
                (date, start, end)
            )

        db.commit()

    all_hours = db.execute(
        'SELECT * FROM opening_hours WHERE date >= date(\'now\') '
        'ORDER BY date ASC'
    )
    today = datetime.date.today()

    return render_template(
        'internal/opening_hours.html',
        opening_hours=all_hours,
        today=today
    )


@bp.post('/opening_hours/delete/<int:n>')
@login_required
def delete_opening_hours(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM opening_hours WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.opening_hours'))


@bp.route('/shifts', methods=('GET', 'POST'))
@login_required
def shifts():
    db = get_db()

    if request.method == 'POST':
        worker = request.form['worker']
        date = request.form['date']
        start = request.form['start']
        end = request.form['end']
        #TODO make this do stuff
        job = request.form['job']

        existing_shift = db.execute(
            'SELECT id FROM shift WHERE date = date(?) AND worker_id = ?',
            (date, worker)
        ).fetchone()
        if existing_shift is None:
            db.execute(
                'INSERT INTO shift '
                '(worker_id, date, start, end)'
                'VALUES (?, date(?), time(?), time(?))',
                (worker, date, start, end)
            )
        else:
            db.execute(
                'UPDATE shift SET start = time(?), end = time(?) WHERE id = ?',
                (start, end, existing_shift['id'])
            )

        db.commit()

    all_workers = db.execute(
        'SELECT * FROM worker ORDER BY display_name ASC'
    ).fetchall()

    default_start = "19:00"
    default_end = "00:00"
    opening_hours_today = db.execute(
        'SELECT * FROM opening_hours WHERE date = date(\'now\')'
    ).fetchone()
    if opening_hours_today is not None:
        default_start = opening_hours_today['start']
        default_end = opening_hours_today['end']

    shifts = db.execute(
        'SELECT date, start, end, '
        'IFNULL(display_name, \'<deleted worker>\') as worker, shift.id as id '
        'FROM shift LEFT OUTER JOIN worker ON worker.id = shift.worker_id '
        'ORDER BY date DESC'
    ).fetchall()

    today = datetime.date.today().isoformat()

    return render_template(
        'internal/shifts.html',
        workers=all_workers,
        default_start=default_start,
        default_end=default_end,
        today=today,
        shifts=shifts
        # TODO
        #jobs=jobs
    )


@bp.post('/shifts/delete/<int:n>')
@login_required
def delete_shifts(n):
    if n is not None:
        db = get_db()
        db.execute('DELETE FROM shift WHERE id = ?', (n,))
        db.commit()

    return redirect(url_for('internal.shifts'))

@bp.route('/print_menu')
@login_required
def print_menu():
    db = get_db()

    category_names = db.execute(
        'SELECT name FROM beer_category ORDER BY id ASC'
    ).fetchall()


    categories = []

    for index, category_name in enumerate(category_names):
        query = (
            'SELECT beer.name as name, style, beer_category.name as category, '
            'country_iso_3166_id as country_code, abv, volume_ml, price_kr '
            'FROM beer INNER JOIN beer_category '
            'ON beer.category_id = beer_category.id '
            'WHERE available = 1 AND beer_category.id = ?'
        )
        category = {
            'name': category_name["name"],
            'beers': db.execute(query, (str(index + 1),)).fetchall()
        }
        categories.append(category)

    foods = db.execute('SELECT * FROM food ORDER BY name ASC').fetchall()
    snacks = db.execute('SELECT * FROM snack ORDER BY name ASC').fetchall()


    tex = render_template(
        'external/menu.tex',
        beer_categories=categories,
        foods=foods,
        snacks=snacks,
    )

    with TemporaryDirectory() as tmpdir:
        try:
            subprocess.run(
                ['pdflatex', '-halt-on-error'],
                cwd=tmpdir,
                capture_output=True,
                check=True,
                input=tex.encode('utf8'),
                timeout=10,
            )
        except subprocess.TimeoutExpired as e:
            return Response(
                (
                    'PDFLaTeX timed out\n\nstdout:\n'
                    + (e.stdout.decode('utf8') or '[no output on stdout]')
                    + '\nstderr:\n'
                    + (e.stderr.decode('utf8') or '[no output on stderr]')
                ),
                mimetype='text/plain'
            )
        except subprocess.CalledProcessError as e:
            return Response(
                (
                    'PDFLaTeX shit itself\n\nstdout:\n'
                    + (e.stdout.decode('utf8') or '[no output on stdout]')
                    + '\nstderr:\n'
                    + (e.stderr.decode('utf8') or '[no output on stderr]')
                ),
                mimetype='text/plain'
            )

        pdf_path = os.path.join(tmpdir, 'texput.pdf')
        with open(pdf_path, 'rb') as pdf:
            return Response(pdf.read(), mimetype='application/pdf')


@ bp.app_template_filter(name='escape_tex')
def escape_tex(s):
    return (
        s.replace('&', '\\&')
        .replace('$', '\\$')
        .replace('%', '\\%')
        .replace('#', '\\#')
        .replace('_', '\\_')
        .replace('{', '\\{')
        .replace('}', '\\}')
        .replace('<', '\\textless{}')
    )
