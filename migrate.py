#!/bin/env python3

import sys
import re

from IPython import embed
import mysql.connector
from pycountry import countries
import sqlite3

if len(sys.argv) != 4:
    print(f'Usage: {sys.argv[0]} MYSQL_USER MYSQL_PASSWORD SQLITE_DB')
    sys.exit(1)

db_credentials = {
    'user': sys.argv[1],
    'password': sys.argv[2],
}

old_conn = mysql.connector.connect(**db_credentials, database='puben_http')
old_cursor = old_conn.cursor()
new_conn = sqlite3.connect(sys.argv[3], detect_types=sqlite3.PARSE_DECLTYPES)

print('Connected to menu DB')
print('Getting beers')


# BEERS
category_lookup = {
    1: 'on_keg',
    2: 'lager',
    3: 'ale',
    4: 'belgian',
    5: 'porter_stout',
    6: 'weiss',
    7: 'lambic',
    8: 'other',
    9: 'wine',
    10: 'cider',
    11: 'nonalcoholic',
    12: 'barleywine',
}

old_cursor.execute('SELECT * FROM puben_prislista_drycker')
beers = []

for id, available, name, style, country_code, abv, volume, price, category_id in old_cursor:
    beer = {
        'available': int(available),
        'name': name.strip(),
        'style': style,
        'country_code': countries.get(alpha_3=country_code).numeric,
        'abv': float(abv.strip('<% ')),
        'volume': -1 if volume == 'Glas' else int(volume),
        'price': int(price),
        'category': category_lookup[category_id],
    }
    beers.append(beer)

print('Inserting beers')

for beer in beers:
    new_conn.execute(
        'INSERT INTO beer (name, style, country_iso_3166_id, abv, volume_ml, '
        'price_kr, available, category_id) VALUES '
        '(?, ?, ?, ?, ?, ?, ?, (SELECT id FROM beer_category WHERE name = ?))',
        (beer['name'], beer['style'], beer['country_code'], beer['abv'],
         beer['volume'], beer['price'], beer['available'], beer['category'])
    )

new_conn.commit()

print(f'Inserted {len(beers)} beers!')
print('Getting foods')


# FOODS
old_cursor.execute('SELECT * FROM puben_prislista_mat')
foods = []

for id, available_wed_thu, available_fri, name, price in old_cursor:
    food = {
        'name': name.strip(),
        'price': int(price),
    }
    if available_wed_thu == 1 and available_fri == 1:
        foods.append(food)

print('Inserting foods')

for food in foods:
    new_conn.execute(
        'INSERT INTO food (name, price_kr)'
        'VALUES (?, ?)',
        (food['name'], food['price'])
    )

new_conn.commit()
print(f'Inserted {len(foods)} foods!')
print('Getting snacks')


# SNACKS
old_cursor.execute('SELECT * FROM puben_prislista_snacks')
snacks = []

for id, available, name, price in old_cursor:
    snack = {
        'name': name.strip(),
        'price': int(price),
    }
    if available == 1:
        snacks.append(snack)

print('Inserting snacks')

for snack in snacks:
    new_conn.execute(
        'INSERT INTO snack (name, price_kr)'
        'VALUES (?, ?)',
        (snack['name'], snack['price'])
    )

new_conn.commit()
print(f'Inserted {len(snacks)} snacks!')


# WORKERS
old_cursor.close()
old_conn.close()
old_conn = mysql.connector.connect(**db_credentials, database='tidslista')
old_cursor = old_conn.cursor()

print('Connected to workers & hours DB')
print('Getting workers')

old_cursor.execute('SELECT * FROM users')
workers = []

status_lookup = {
    1: 'worker',
    2: 'worker_public',
    3: 'ex_worker',
    4: 'ex_worker',
    5: 'ex_worker',
}

for id, name, first_name, last_name, phone, mobile, ip, email, status, personal_number, address, note in old_cursor:
    worker = {
        'display_name': name.strip(),
        'first_name': first_name.strip() if first_name else 'UNKNOWN',
        'last_name': last_name.strip() if last_name else 'UNKNOWN',
        'telephone': mobile or phone,
        'email': email.strip() if email else 'UNKNOWN',
        'address': address.strip() if address else None,
        'note': note.strip() if note else None,
        'status': status_lookup[status],
    }
    workers.append(worker)

print('Inserting workers')

for worker in workers:
    new_conn.execute(
        'INSERT INTO worker (display_name, first_name, last_name, telephone, '
        'email, address, note, status_id) '
        'VALUES '
        '(?, ?, ?, ?, ?, ?, ?,(SELECT id FROM worker_status WHERE name = ?))',
        (worker['display_name'], worker['first_name'], worker['last_name'],
         worker['telephone'], worker['email'], worker['address'],
         worker['note'], worker['status'])
    )

new_conn.commit()
print(f'Inserted {len(workers)} workers!')
