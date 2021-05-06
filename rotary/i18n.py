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
        'work' : 'Work',
        'language' : '🇸🇪',
    },
    'index': {
        'tagline': '…to the pub run by students with prices suited for students open for everyone in central Gothenburg.',
        'news': {
            'header': 'Latest updates',
        },
        'opening_hours': 'Opening Hours',
        'closed': 'closed',
    },
    'menu': {
        'beer_categories': {
            'on_keg': 'On Keg',
            'lager': 'Lagers',
            'ale': 'Ales',
            'porter_stout': 'Porters & Stouts',
            'weiss': 'Weißbiers',
            'barleywine': 'Barley Wines',
            'belgian': 'Belgians',
            'lambic': 'Lambics',
            'other': 'Other',
            'wine': 'Wines',
            'cider': 'Ciders',
            'nonalcoholic': '< 2.25% abv',
        },
        'drinks' : 'Drinks',
        'food' : 'Food',
        'snacks' : 'Snacks',
        'name' : 'Name',
        'abv' : 'ABV',
        'country' : 'Country',
        'volume' : 'Volume',
        'price' : 'Price',
    },
    'contact': {
        'header': 'Contact Us',
        'text': 'Use form below',
        'submit': 'Submit',
        'email': 'Email',
        'message': 'Message',
    },
    'days' : ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'work' : {
        'header' : 'Working at Rotary Pub',
        'text' : 'Do you also like Rotary? Why not <strong>work here</strong>!<br>'
        },
}

strings_sv = {
    'nav': {
        'index': 'Hem',
        'menu': 'Meny',
        'contact': 'Kontakt',
        'work' : 'Jobba',
        'language' : '🇬🇧'
    },
    'index': {
        'tagline': '…till den studentdrivna puben med studentförmånliga priser för alla mitt i Göteborg.',
        'news': {
            'header': 'Senaste nytt',
        },
        'opening_hours': 'Öppettider',
        'closed': 'stängt',
    },
    'menu': {
        'beer_categories': {
            'on_keg': 'På Fat',
            'lager': 'Lager',
            'ale': 'Ale',
            'porter_stout': 'Porter & Stout',
            'weiss': 'Weißbier',
            'barleywine': 'Barley Wine',
            'belgian': 'Belgare',
            'lambic': 'Lambics',
            'other': 'Random Annat',
            'wine': 'Vin',
            'cider': 'Cider',
            'nonalcoholic': '< 2.25% alkohol',
        },
        'drinks' : 'Dryck',
        'food' : 'Mat',
        'snacks' : 'Snacks',
        'name' : 'Namn',
        'abv' : 'ABV',
        'country' : 'Land',
        'volume' : 'Volym',
        'price' : 'Pris',
    },
    'contact': {
        'header': 'Kontakta oss',
        'text': 'Använd formuläret nedan',
        'submit': 'Skicka',
        'email': 'Epost',
        'message': 'Meddelande',
    },
    'days' : ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag'],
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
