from flask import Blueprint, g, render_template, request, session
from datetime import date, timedelta

from rotary.db import get_db

bp = Blueprint('external', __name__, template_folder='templates/external')


@bp.route('/')
def index():
    db = get_db()
    query = None
    english = session.get('english')

    if english:
        query = (
            'SELECT date(time) as day, title_en as title, body_en as body '
            'FROM news ORDER BY time DESC LIMIT 1'
        )
    else:
        query = (
            'SELECT date(time) as day, title_sv as title, body_sv as body '
            'FROM news ORDER BY time DESC LIMIT 1'
        )

    news = db.execute(query).fetchone()

    today = date.today()
    days_after_monday = today.weekday()
    monday = today - timedelta(days=days_after_monday)

    opening_hours = []
    closed_string = ''

    for i in range(7):
        day = monday + timedelta(days=i)
        result = db.execute(
            'SELECT start, end FROM opening_hours WHERE date = ?',
            (day.isoformat(),)
        ).fetchone()
        day = day.strftime('%d/%m')

        if result is None:
            opening_hours.append(
                {
                    'date': day,
                    'hours': None,
                }
            )
        else:
            start, end = result
            opening_hours.append(
                {
                    'date': day,
                    'hours': f'{start}-{end}',
                }
            )

    return render_template('index.html', news=news, opening_hours=opening_hours)


@bp.route('/contact', methods=('GET', 'POST'))
def contact():
    if request.method == 'GET':
        return render_template('contact.html', submitted=False)
    else:
        # TODO: Handle the form data
        return render_template('contact.html', submitted=True)

@bp.route('/work')
def work():
    return render_template('work.html')

@bp.route('/menu')
def menu():
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

    return render_template('menu.html', beer_categories=categories, foods=foods, snacks=snacks)
