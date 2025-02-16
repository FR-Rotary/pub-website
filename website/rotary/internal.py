import os
import random
import datetime

from flask import Blueprint, render_template, redirect, request, url_for, jsonify, current_app
from pycountry import countries
from werkzeug.utils import secure_filename

from rotary.db import get_db
from rotary.auth import login_required
from rotary.i18n import strings_en
from rotary.utils.util import dict_from_row
from rotary.utils.menu import generate_pdf, fetch_menu_data

bp = Blueprint('internal', __name__, url_prefix='/internal')

@bp.route('')
@login_required
def index():
    # Call the existing randomize_comic_strip function
    directory = 'rotary/static/images/comics/'
    try:
        files = os.listdir(directory)
        if files:
            random_file = random.choice(files)
            comic_strip_url = os.path.join('/static/images/comics/', random_file)
        else:
            comic_strip_url = None
    except Exception as e:
        comic_strip_url = None
    # Pass the comic strip URL to the template
    return render_template('internal/index.html', comic_strip_url=comic_strip_url)

@bp.route('/')
@login_required
def index_slash_redirect():
    return redirect(url_for('internal.index'))

# Add/Display beers
@bp.route('/beers', methods=('GET', 'POST'))
@login_required
def beers():
    db = get_db()

    if request.method == 'POST':
        try:
            db.execute(
                'INSERT INTO beer (name, style, country_iso_3166_id, abv, volume_ml, price_kr, category_id, available) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    request.form['name'],
                    request.form['style'],
                    request.form['country_code'],  # Assuming validation for non-int type
                    float(request.form['abv'].replace(',', '.')),
                    int(request.form['volume']),
                    int(request.form['price']),
                    int(request.form['category_id']),
                    1 if request.form.get('available') else 0,
                )
            )
            db.commit()
        except db.DatabaseError as e:
            db.rollback()

    beers = db.execute(
        'SELECT b.available, b.name, b.id, b.style, b.abv, b.country_iso_3166_id, b.volume_ml, b.price_kr, '
        'IFNULL(bc.name_sv, \'<unknown category>\') as category '
        'FROM beer b '
        'LEFT JOIN beer_category bc ON b.category_id = bc.id '
        'ORDER BY b.name ASC'
    ).fetchall()
    
    # Fetch categories only if needed for other parts of the template
    categories = db.execute(
        'SELECT id, name_sv AS name, name_en, priority FROM beer_category ORDER BY priority ASC'
    ).fetchall()

    return render_template(
        'internal/beers.html',
        beers=beers,
        countries=countries,
        categories=categories,
        category_names={category['id']: category['name'] for category in categories}
    )

@bp.route('/beers/edit/<int:n>', methods=('GET', 'POST'))
@login_required
def edit_beer(n):
    if request.method == 'POST' and n is not None:
        db = get_db()

        name = request.form['name']
        style = request.form['style']
        country_code = request.form['country_code']     #DO NOT TYPECAST THIS TO INT!
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
            f'SELECT id, name_sv AS name FROM beer_category ORDER BY id ASC'
        ).fetchall()

        return render_template(
            'internal/edit_beer.html',
            beer = beer,
            countries=countries,
            categories=categories,
            category_names={category['id']: category['name'] for category in categories}
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
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
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
    available = 1 if request.form.get('available') else 0

    db.execute( 'INSERT INTO food (name, price_kr, available) VALUES (?,?,?)', (name, price, available))
    db.commit()

    return redirect(url_for('internal.food'))

@bp.route('/food/edit/<int:n>', methods=['GET', 'POST'])
def edit_food(n):
    if request.method == 'POST' and n is not None:
        db = get_db()
        name = request.form['name']
        price = int(request.form['price'])
        available = 1 if request.form.get('available') else 0

        db.execute(
            'UPDATE food SET '
            'name = ?, price_kr = ?, available = ?'
            'WHERE id = ?',
            (name, price, available, n)
        )
        db.commit()
        return redirect(url_for('internal.food')) 

    if n is not None:
        db = get_db()
        food = db.execute('SELECT * FROM food WHERE id = ?', (n,)).fetchone()
        
        return render_template(
                'internal/edit_food.html', 
                food=food)

    return redirect(url_for('internal.food'))

@bp.post('/food/toggle/<int:n>')
@login_required
def toggle_food(n):
    if n is not None:
        db = get_db()
        db.execute('UPDATE food SET available = NOT available WHERE id = ?', (n,))
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
    available = 1 if request.form.get('available') else 0

    db.execute('INSERT INTO snack (name, price_kr, available) VALUES (?,?,?)', (name, price, available))
    db.commit()

    return redirect(url_for('internal.food'))

@bp.route('/snack/edit/<int:n>', methods=['GET', 'POST'])
def edit_snack(n):
    if request.method == 'POST' and n is not None:
        db = get_db()
        name = request.form['name']
        price = int(request.form['price'])
        available = 1 if request.form.get('available') else 0

        db.execute(
            'UPDATE snack SET '
            'name = ?, price_kr = ?, available = ?'
            'WHERE id = ?',
            (name, price, available, n)
        )
        db.commit()
        return redirect(url_for('internal.food')) 

    if n is not None:
        db = get_db()
        snack = db.execute('SELECT * FROM snack WHERE id = ?', (n,)).fetchone()
        
        return render_template(
                'internal/edit_snack.html', 
                snack=snack)

    return redirect(url_for('internal.food'))

@bp.post('/snack/toggle/<int:n>')
@login_required
def toggle_snack(n):
    if n is not None:
        db = get_db()
        db.execute('UPDATE snack SET available = NOT available WHERE id = ?', (n,))
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

@bp.route('/categories/edit/<int:n>', methods=('GET', 'POST'))
@login_required
def edit_category(n):
    db = get_db()
    
    if request.method == 'POST':
        db.execute(
            'UPDATE beer_category SET name_sv = ?, name_en = ?, priority = ? WHERE id = ?',
            (request.form['name_sv'], request.form['name_en'], request.form['priority'], n)
        )
        db.commit()
        return redirect(url_for('internal.beers'))

    category = db.execute('SELECT * FROM beer_category WHERE id = ?', (n,)).fetchone()
    return render_template('internal/edit_category.html', category=category) if category else redirect(url_for('internal.beers'))

@bp.post('/categories/add')
@login_required
def add_category():
    if request.method == 'POST':
        db = get_db()

        name_sv = request.form['name_sv']
        name_en = request.form['name_en']
        priority = int(request.form['priority'])

        db.execute(
            'INSERT INTO beer_category (name_sv, name_en, priority) '
            'VALUES (?, ?, ?)',
            (name_sv, name_en, priority)
        )
        db.commit()
    
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
    ## Create new worker
    if request.method == 'POST':
        display_name = request.form['display_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        telephone = request.form['telephone']
        p_id = request.form['personal_id_number']
        email = request.form['email']
        address = request.form['address']
        note = request.form['note']
        status_id = request.form['status_id']

        db.execute(
            'INSERT INTO worker '
            '(display_name, first_name, last_name, '
            'telephone, personal_id_number, email, '
            'address, note, status_id) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (display_name, first_name, last_name,
             telephone, p_id, email, address, note, status_id)
        )
        db.commit()

        return redirect(url_for('internal.workers'))
    ## Provide all current workers
    else:
        all_workers = db.execute('SELECT * FROM worker ORDER BY display_name ASC').fetchall()
        worker_status = db.execute('SELECT * FROM worker_status').fetchall()
        return render_template('internal/workers.html', workers=all_workers, worker=None, worker_status=worker_status)


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
        personal_id_number = request.form['personal_id_number']
        telephone = request.form['telephone']
        email = request.form['email']
        address = request.form['address']
        note = request.form['note']
        status_id = request.form['status_id']

        db.execute(
            'UPDATE worker SET '
            'display_name = ?, first_name = ?, last_name = ?, '
            'personal_id_number = ?, telephone = ?, '
            'email = ?, address = ?, note = ?, status_id = ? '
            'WHERE id = ?',
            (display_name, first_name, last_name, personal_id_number, telephone, email, address,
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
        worker_ids = request.form.getlist('workerid[]')
        date = request.form['date']
        start, end = request.form['start'], request.form['end']
        shift_types = request.form.getlist('shift_type[]')

        for worker_id, shift_type in zip(worker_ids, shift_types):
            existing_shift = db.execute(
                'SELECT id FROM shift WHERE date = date(?) AND worker_id = ?',
                (date, worker_id)
            ).fetchone()
            if existing_shift is None:
                db.execute(
                    'INSERT INTO shift '
                    '(worker_id, date, start, end, shift_type_id)'
                    'VALUES (?, date(?), time(?), time(?), ?)',
                    (worker_id, date, start, end, shift_type)
                )
            else:
                db.execute(
                    'UPDATE shift SET start = time(?), end = time(?), shift_type_id = ? WHERE id = ?',
                    (start, end, shift_type, existing_shift['id'])
                )
        db.commit() 
        return redirect(url_for("internal.shifts"))

    all_workers = db.execute( 
        'SELECT * FROM worker ORDER BY display_name ASC'
    ).fetchall()
    all_workers = [dict_from_row(worker) for worker in all_workers]

    default_start = "17:00"
    default_end = "01:00"

    shifts = db.execute(
        'SELECT st.name AS type, '
        'IFNULL(w.display_name, \'<deleted worker>\') AS worker, '
        'IFNULL(w.first_name, \'<deleted worker>\') AS worker_first_name, '
        'IFNULL(w.last_name, \'<deleted worker>\') AS worker_last_name, '
        'IFNULL(w.personal_id_number, \'<deleted worker>\') AS worker_personal_id_number, '
        's.date, s.start, s.end, s.id '
        'FROM shift s '
        'LEFT JOIN worker w ON w.id = s.worker_id '
        'LEFT JOIN shift_type st ON st.id = s.shift_type_id '
        'ORDER BY s.date DESC'
    ).fetchall()

    today = datetime.date.today().isoformat()

    shift_types = db.execute(
        'SELECT id, name FROM shift_type'
    ).fetchall()

    return render_template(
        'internal/shifts.html',
        all_workers=all_workers,
        default_start=default_start,
        default_end=default_end,
        today=today,
        shifts=shifts,
        shift_types=shift_types
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
    categories, foods, snacks = fetch_menu_data()
    tex = render_template(
        'external/menu.tex',
        beer_categories=categories,
        foods=foods,
        snacks=snacks,
    )
    return generate_pdf(tex)


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

@bp.route('/internal/upload_comic_strip', methods=['POST'])
@login_required
def upload_comic_strip():
    # Handle the case where no file part is provided
    if 'comic_strip' not in request.files:
        print("No file part")
        return redirect(url_for('internal.index'))
    file = request.files['comic_strip']
    # Handle the case where no file is selected
    if file.filename == '':
        return redirect(url_for('internal.index'))
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join('rotary/static/images/comics/', filename)
        directory = os.path.dirname(save_path)
        # Create directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        file.save(save_path)
        # Optionally, update the database or perform other actions
        return redirect(url_for('internal.index'))
