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
        'rentals' : 'Rentals',
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
    'rentals': {
        'header': 'Renting Rotary Pub',
        'intro': {
                'text': 'Rotary Pub is available for rental arrangements for private parties. We have long experience of throwing e.g. 25th/30th anniversaries and graduation parties. Rentals normally takes place on Saturdays between September-June. The two most common types of rentals that we offer are described below. For more extensive information contact us via the form below. We can incorporate many variations on your request; examples that we have offered before include live bands, DJs, karaoke, etc.',
            },
        'sections': {
            'sittning': {
                'header': 'Three Course Dinner',
                'content': 'The most common alternative. Three courses including wine are served. The premises are available from agreed upon time until 03 at latest. Our personnel suggest a menu that is discussed with the renting party. Alternatives for different price levels are available. The food is prepared by us on location and our staff handles all the work. Underage people are allowed to be in the premises, of course as long as they are not served any alcohol.',
            },
            'bar': {
                'header': 'Bar rental',
                'content': 'The pub with bar staff is rented without a formal dinner taking place. A regular pub menu can be offered, either with pizza and hamburgers or a buffet. Perfect for a more relaxed party similar to a night out at the pub where only the coolest people are invited, your friends! Since the pub is rented without food, the renter only pays the rent for the premises.',
            },
            'pricing': {
                'header': 'Pricing',
                'content': 'The rental fee is always 5500 kr for a night. That includes staff for the entire evening and cleaning after. For the three course dinner it usually costs around 200 kr/person for both food and drinks, but we offer menus in a wide variety of price ranges.',
            },
            'rules': {
                'header': 'Rules',
                'content': 'There are no rules /s',
            },
        },
        
        'submit': 'Send',
        'email': 'Your email address',
        'subject': 'Subject',
        'message': 'Message',
        'body_placeholder': 'Write your message here',
        'captcha': 'CAPTCHA: In which city is Rotary Pub locates?',
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
        'rentals' : 'Hyra puben',
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
    'rentals': {
        'header': 'Hyra Rotary Pub',
        'intro': {
                'text': 'Rotary Pub är tillgänglig för uthyrning till privata sällskap. Vi har lång erfarenhet av att anordna exempelvis 25/30-års-, examens- och disputationskalas. Uthyrningar sker vanligen på lördagar mellan September-Maj men specifikt datum koms överens mellan den som hyr och uthyrningsansvarig som går att nå genom kontaktforumläret längst ner på sidan. Vi kan tillmötesgå många variationer och har som exempel haft liveband, DJs, karaokeafton m.m. Notera dock att oftast behöver den som hyr arrangera detta själv då vi inte har utrustning för DJ eller kareoke (vi kan dock hjälpa att hitta vettiga ställen för att hyra detta).',
            },
        'sections': {
            'sittning': {
                'header': 'Trerätters middag',
                'content': 'Trerätters middag med eventuell dryck serveras. Lokalen är tillgänglig från överenskommen tid till senast 03. Vår personal föreslår en matmeny som sedan diskuteras med det hyrande sällskapet. Alternativ för olika prisbilder finns. Maten tillagas av oss på plats och vår personal står för alla arbetsuppgifter. Vi dukar upp för sittning i lokalen och rekommenderat maxantal är 50 sittande gäster, annars blir det väldigt trångt. Minderåriga får befinna sig i lokalen, givetvis så länge de inte serveras alkohol.',
                'caption': 'En uppdukning för ett mindre sällskap.'
            },
            'bar': {
                'header': 'Baruthyrning',
                'content': 'Lokal med barpersonal hyrs utan att en anordnad middag sker. Vanlig pubmeny kan erbjudas antingen med pizza och hamburgare eller buffé. Perfekt för en lite mer avslappnad fest liknande en kväll på krogen där bara de mest sköna får komma, dina kompisar! Då puben hyrs utan mat betalar uthyraren endast lokalhyran.',
            },
            'pricing': {
                'header': 'Prissättning',
                'content': 'Oberoede av upplägg är hyran 5500 kr för en kväll. Då ingår alltid personal för hela kvällen samt städ efteråt. Beroende på upplägg tillkommer kostnader för mat och dryck, vid en normal trerättersmiddag kan man räkna med att det kostar 200 kr/person för både mat och dryck.',
            },
            'rules': {
                'header': 'Regler',
                'content': 'Det finns inga regler, vi lever i anarki /s',
            },
        },
        
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
