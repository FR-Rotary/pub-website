import functools

from flask import (
    Blueprint, current_app, g, redirect,
    render_template, request, session, url_for,
)

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (
            username is not None and
            password is not None and
            username == current_app.config["USERNAME"] and
            password == current_app.config["PASSWORD"]
        ):
            # Correct login
            session.clear()
            session['authenticated'] = True
            return redirect(url_for('external.index'))
        else:
            # Wrong login
            return render_template('internal/login.html', login_failed=True)
    elif g.authenticated:
        return redirect(url_for('internal.index'))
    else:
        return render_template('internal/login.html', login_failed=False)

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('external.index'))


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
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
