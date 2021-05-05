import functools

from flask import (
    Blueprint, current_app, flash, g, redirect,
    render_template, request, session, url_for,
)
from rotary.db import get_db

bp = Blueprint('i18n', __name__)

strings_en = {

}

strings_sv = {
    'nav': {
        'index': 'Home',
        'menu': 'Menu',
        'contact': 'Contact',
    },
}

@bp.route('/toggle_language')
def toggle():
    return "Toggle not yet implemented"


@bp.before_app_request
def get_authentication_status():
    english = session.get('english')

    if english:
        g.strings = strings_en
    else:
        g.strings = strings_sv
