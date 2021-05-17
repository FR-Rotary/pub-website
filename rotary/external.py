from flask import Blueprint, g, render_template, request, session, current_app
from datetime import date, timedelta

from rotary.util import dict_from_row
from rotary.db import get_db
from rotary.mail import Mail, Server

bp = Blueprint('external', __name__)


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

    return render_template(
        'external/index.html',
        news=news,
        opening_hours=opening_hours
    )


@bp.route('/contact', methods=('GET', 'POST'))
def contact():
    if request.method == 'GET':
        return render_template('external/contact.html')
    else:
        email = request.form['email']
        subject = request.form['subject']
        body = request.form['body']
        captcha = request.form['captcha']

        if captcha.strip().lower() not in [
                'gothenburg', 'göteborg', 'goteborg'
        ]:
            return render_template(
                'external/contact.html',
                email=email,
                body=body,
                subject=subject,
                captcha=captcha,
                captcha_failed=True
            )

        # Get config for server
        host = current_app.config['SMTP_HOST']
        user = current_app.config['SMTP_USERNAME']
        password = current_app.config['SMTP_PASSWORD']

        if host is None or user is None or password is None:
            return "Error: SMTP is not configured"

        # config server
        s = Server(
            user,
            password,
            host
        )

        # compose message
        m = Mail(
            'website@rotarypub.se',
            'juliusschumacher@gmail.com',
            subject,
            body,
            reply_to=email
        )

        # send message
        s.send(m)

        return render_template('external/contact.html', submitted=True)


@bp.route('/work')
def work():
    return render_template('external/work.html')


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

    # add alcohol per krona for logged in users
    for i, category in enumerate(categories):
        for j, beer in enumerate(category['beers']):
            beer = dict_from_row(beer)
            beer['apk'] = format(beer['volume_ml'] *
                                 (beer['abv'] / 100) / beer['price_kr'], '.3f')
            categories[i]['beers'][j] = beer

    foods = db.execute('SELECT * FROM food ORDER BY name ASC').fetchall()
    snacks = db.execute('SELECT * FROM snack ORDER BY name ASC').fetchall()

    return render_template(
        'external/menu.html',
        beer_categories=categories,
        foods=foods,
        snacks=snacks
    )


@bp.before_app_request
def update_beer_count():
    beer_count = session.get('beer_count')
    if beer_count is None:
        current_app.logger.info('Updating beer count')
        db = get_db()
        count = db.execute(
            'SELECT COUNT(*) FROM beer INNER JOIN beer_category '
            'ON beer.category_id = beer_category.id '
            'WHERE available = 1 AND '
            'beer_category.name NOT IN (\'wine\', \'cider\', \'nonalcoholic\')'
        ).fetchone()
        session['beer_count'] = int(dict_from_row(count)['COUNT(*)'])

    g.beer_count = session.get('beer_count', 'some unknown amount of')
