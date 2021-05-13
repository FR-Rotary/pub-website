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
        'find' : 'Find Us',
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
        'text': 'Use the form below to send us an email',
        'submit': 'Submit',
        'email': 'Your email address',
        'message': 'Message',
        'body_placeholder': 'Write your message here',
        'captcha': 'CAPTCHA: In which city is Rotary Pub located?',
        'captcha_placeholder': 'Somethingtown',
        'captcha_failed': 'That\'s the wrong answer!',
        'thanks': 'Thanks for contacting us! We\'ll get back to you as soon as possible.',
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
        'find' : 'Hitta oss',
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
        'text': 'Använd formuläret nedan för att skicka ett mail till oss',
        'submit': 'Skicka',
        'email': 'Din mailadress',
        'message': 'Meddelande',
        'body_placeholder': 'Skriv ditt meddelande här',
        'captcha': 'CAPTCHA: I vilken stad ligger Rotary Pub?',
        'captcha_placeholder': 'Nåntingstad',
        'captcha_failed': 'Fel svar!',
        'thanks': 'Tack för att du kontaktade oss! Vi återkommer så snart som möjligt.',
    },
    'work' : {
        'header' : 'Working at Rotary Pub',
        'text' : 'Do you also like Rotary? Why not <strong>work here</strong>!<br>'
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
