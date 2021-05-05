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


@bp.route('/menu')
def menu():
    db = get_db()

    categories = db.execute('SELECT name FROM beer_category ORDER BY id ASC')
    beers = {}

    for category in categories:
        q = (
            'SELECT beer.name as name, style, beer_category.name as category, '
            'country_iso_3166_id as country, abv, volume_ml as volume '
            'FROM beer INNER JOIN beer_category '
            'ON beer.category_id = beer_category.id '
            f'WHERE available = 1 AND beer_category.name = \'{category["name"]}\''
        )
        print(q)
        beers[category] = db.execute(
            q
        ).fetchall()

    return render_template('menu.html', beers=beers)

    # SELECT beer.name as name, style, beer_category.name as category, country_iso_3166_id as country, abv, volume_ml as volume FROM beer INNER JOIN beer_category ON beer.category_id = beer_category.id WHERE available = 1 AND beer_category.name = 'porter_stout';
