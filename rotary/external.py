from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from rotary.auth import login_required
from rotary.db import get_db

bp = Blueprint('external', __name__)


@bp.route('/')
def index():
    db = get_db()
    news = db.execute(
        'SELECT date(time) as day, title, body FROM news ORDER BY time DESC LIMIT 1'
    ).fetchone()

    return render_template('index.html', news=news)


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
            f'WHERE available = 1 AND beer_category.id = \'{index + 1}\''
        )
        category = {
            'name': category_name["name"],
            'beers': db.execute(query).fetchall()
        }
        categories.append(category)

    foods = db.execute('SELECT * FROM food ORDER BY name ASC').fetchall()
    snacks = db.execute('SELECT * FROM snack ORDER BY name ASC').fetchall()

    return render_template('menu.html', beer_categories=categories, foods=foods, snacks=snacks)
