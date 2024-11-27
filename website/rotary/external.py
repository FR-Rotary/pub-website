from datetime import date, timedelta

from flask import (
    Blueprint, g, render_template, request, session, current_app, Response
)

from rotary.utils.util import dict_from_row, format_time
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
            start = format_time(start)
            end = format_time(end)
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

def handle_form_submission(email, body, subject):
    # Get config for server
    host = current_app.config['SMTP_HOST']
    user = current_app.config['SMTP_USERNAME']
    password = current_app.config['SMTP_PASSWORD']
    list_address = current_app.config['CONTACT_FORM_ADDRESS']

    if (host is None or user is None or password is None or list_address is None):
        return False

    server = Server(user, password, host)
    message = Mail(user, list_address, subject, body, reply_to=email)
    server.send(message)

    return True

@bp.route('/contact', methods=('GET', 'POST'))
def contact():
    if request.method == 'POST':
        # Extract form data
        email = request.form['email']
        body = request.form['body']
        subject = request.form['subject']
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

        if handle_form_submission(email, body, subject):
            return render_template('external/contact.html', submitted=True)
        else:
            return "Error: SMTP is not configured"

    return render_template('external/contact.html')

@bp.route('/rentals', methods=('GET', 'POST'))
def rentals():
    if request.method == 'POST':
        # Extract form data specific to rentals
        email = request.form['email']
        body = request.form['body']
        subject = request.form['subject']
        captcha = request.form['captcha']

        if captcha.strip().lower() not in [
                'gothenburg', 'göteborg', 'goteborg'
        ]:
            return render_template(
                'external/rentals.html',
                email=email,
                body=body,
                subject=subject,
                captcha=captcha,
                captcha_failed=True
            )

        # Handle form submission for rentals
        if handle_form_submission(email, body, subject):
            return render_template('external/rentals.html', submitted=True)
        else:
            return "Error: SMTP is not configured"

    return render_template('external/rentals.html')


@bp.route('/work')
def work():
    return render_template('external/work.html')


@bp.route('/menu')
def menu():
    db = get_db()

    name_column = 'name_en' if session.get('english') else 'name_sv'

    category_names = db.execute(
        f'SELECT id, {name_column} as name FROM beer_category ORDER BY priority ASC'
    ).fetchall()

    categories = []

    for category_name in category_names:
        query = (
            f'SELECT beer.name as name, style, beer_category.{name_column} as category, '
            'country_iso_3166_id as country_code, abv, volume_ml, price_kr '
            'FROM beer INNER JOIN beer_category '
            'ON beer.category_id = beer_category.id '
            'WHERE available = 1 AND beer_category.id = ?'
            'ORDER BY beer.name ASC'
        )
        category = {
            'name': category_name["name"],
            'beers': db.execute(query, (category_name["id"],)).fetchall()
        }
        categories.append(category)

    # add alcohol per krona for logged in users
    for i, category in enumerate(categories):
        for j, beer in enumerate(category['beers']):
            beer = dict_from_row(beer)
            beer['apk'] = format(beer['volume_ml'] *
                                 (beer['abv'] / 100) / beer['price_kr'], '.3f')
            categories[i]['beers'][j] = beer

    foods = db.execute('SELECT * FROM food WHERE available = 1 ORDER BY name ASC').fetchall()
    snacks = db.execute('SELECT * FROM snack WHERE available = 1 ORDER BY name ASC').fetchall()

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
            'SELECT COUNT(*) FROM beer '
            'WHERE available = 1 AND '
            'category_id NOT IN (9, 10, 11)'
        ).fetchone()
        session['beer_count'] = count[0]

    g.beer_count = session.get('beer_count', 'some unknown amount of')
