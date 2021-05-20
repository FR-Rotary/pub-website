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
        'welcome' : "Welcome",
        'tagline': 'to the pub run by students open for everyone in central Gothenburg.',
        'description' : "Come in, take a seat and pick from our selection of food and drink! We have an amazing selection of craft beer at student friendly prices, rivaling most pubs in town! Our famous pizza is large enough to feed two hungry students, but so tasty you'll want it all for yourself. On fridays we usually offer a buffet as well!",
        'rent' : 'Renting the Pub',
        'rent_text' : 'Did you know you can rent Rotary Pub? Perfect for birthdays, graduations, or just that party you are looking to throw! Want to know more?',
        'contact_us' : 'Contact Us!',
        'work' : 'Working at Rotary Pub',
        'work_text' : 'Do you also love Rotary Pub? Why not',
        'work_link' : 'work here!',
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
        'subject': 'Subject',
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
        'text' : 'Do you also like Rotary? Why not work here!',
        'reasons' : [
            'Staff Discounts!',
            'Friendly People!',
            'Food while you work!',
            'Meet new people!',
            'Volunteering looks good on your resume!',
            'Close to your home (if you live here)!',
            'Get working experience!',
            "You dont need to know anything!",
            "It's completely free!!!"
        ],
        'interested' : 'Sound interesting?',
        'contact' : 'Send us an email',
        'mondays' : 'or show up at one of our monday meetings at 18k Just enter through the kitchen!'
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
        'welcome' : "Välkommen",
        'tagline': 'till den studentdrivna puben för alla mitt i Göteborg!',
        'description' : "Kom in, slå dig ner och välj i vårat sortiment av mat och dryck! Vårat otroliga utbud av öl till studentvänliga priser kan mäta sig med de flesta av stans krogar! Våran berömda pizza är stor nog att mätta två hungriga studenter men så god att du kommer vilja ha den helt för dig själv. På fredagar brukar vi även servera en buffe!",
        'rent' : 'Hyra Puben',
        'rent_text' : 'Visste du att du kan hyra Rotary Pub? Perfekt för födelsedagar, examen eller den där festen du tänkte ha! Vill du veta mer?',
        'contact_us' : 'Kontakta Oss!',
        'work' : 'Jobba på Rotary Pub',
        'work_text' : 'Älskar du också Rotary Pub? Varför inte',
        'work_link' : 'jobba här!',
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
        'subject': 'Titel',
        'message': 'Meddelande',
        'body_placeholder': 'Skriv ditt meddelande här',
        'captcha': 'CAPTCHA: I vilken stad ligger Rotary Pub?',
        'captcha_placeholder': 'Nåntingstad',
        'captcha_failed': 'Fel svar!',
        'thanks': 'Tack för att du kontaktade oss! Vi återkommer så snart som möjligt.',
    },
    'work' : {
        'header' : 'Jobba på Rotary Pub',
        'text' : 'Gillar du också Rotary Pub? Varför inte jobba här?',
        'reasons' : [
            'Personalpriser!',
            'Gött umgänge!',
            'Mat när du jobbar!',
            'Träffa nytt folk!',
            'Ideelt arbete ser bra ut på CV:t',
            'Nära hem (ifall du bor här)!',
            'Samla arberslivserfarenhet!',
            'Du behöver inte kunna ett skit!',
            "Helt Gratis!!!!"
        ],
        'interested' : 'Låter det interessant?',
        'contact' : 'Skicka ett mail',
        'mondays' : 'eller kom på ett måndagsmöte 18:00. Gå bara in igenom köket!'
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
