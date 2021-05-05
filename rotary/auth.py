import functools

from flask import (
    Blueprint, current_app, flash, g, redirect,
    render_template, request, session, url_for,
)
from rotary.db import get_db

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if (username is None or
                password is None or
                username != current_app.config["USERNAME"] or
                current_app.config["PASSWORD"]):
            error = 'Incorrect username or password'

        if error is None:
            session.clear()
            session['authenticated'] = True
            return redirect(url_for('internal'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def get_authentication_status():
    authenticated = session.get('authenticated')

    if authenticated is None:
        g.authenticated = False
    else:
        g.authenticated = authenticated

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.authenticated:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
