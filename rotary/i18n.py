import functools

from flask import (
    Blueprint, current_app, flash, g, redirect,
    render_template, request, session, url_for,
)
from rotary.db import get_db

bp = Blueprint('i18n', __name__)

strings_en = {
    'nav': {
        'index': 'Home',
        'menu': 'Menu',
        'contact': 'Contact',
    },
    'contact' : {
        'header' : 'Contact Us',
        'text' : 'Use form below',
        'submit' : 'Submit',
        'email' : 'Email',
        'message' : 'Message',
    },
}

strings_sv = {
    'nav': {
        'index': 'Hem',
        'menu': 'Meny',
        'contact': 'Kontakt',
    },
    'contact' : {
        'header' : 'Kontakta oss',
        'text' : 'Använd formuläret nedan',
        'submit' : 'Skicka',
        'email' : 'Epost',
        'message' : 'Meddelande',
    },
}

@bp.route('/language')
def toggle_language():
    # Return to / if we don't have a location to return to for some reason
    return_to = request.args.get('r', '/')

    english = session.get('english')
    if english:
        session['english'] = False
    else:
        session['english'] = True

    return redirect(return_to)


@bp.before_app_request
def set_language():
    english = session.get('english')

    if english:
        g.strings = strings_en
    else:
        g.strings = strings_sv
