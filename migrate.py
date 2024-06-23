#!/bin/env python3

import sys
import datetime
import sqlite3

import mysql.connector
from pycountry import countries

if len(sys.argv) != 5:
    print(f'Usage: {sys.argv[0]} MYSQL_USER MYSQL_PASSWORD MYSQL_HOST SQLITE_DB')
    sys.exit(1)

db_credentials = {
    'user': sys.argv[1],
    'password': sys.argv[2],
    'host': sys.argv[3],
}

old_conn = mysql.connector.connect(**db_credentials, database='puben_http')
old_cursor = old_conn.cursor()
new_conn = sqlite3.connect(sys.argv[4], detect_types=sqlite3.PARSE_DECLTYPES)

print('Connected to menu DB')

# BEERS CATEGORIES
print('Getting beer categories')
old_cursor.execute('SELECT * FROM puben_prislista_kategorier')
categories = []
category_lookup = {}

for id, name, eng_name, order in old_cursor:
    category = {
        'name': name,
        'priority': int(order)
    }
    category_lookup[id] = name
    categories.append(category)

print('Inserting beer categories')
for category in categories:
    print(category)
    new_conn.execute(
        'INSERT INTO beer_category (name, priority) VALUES'
        '(?, ?)',
        (category['name'],category['priority'])
    )
new_conn.commit()

print(f'Inserted {len(categories)} categories!')

# BEERS
print('Getting beers')

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

# FOODS
print('Getting foods')


old_cursor.execute('SELECT * FROM puben_prislista_mat')
foods = []

for id, available_wed_thu, available_fri, name, price in old_cursor:
    food = {
        'name': name.strip(),
        'price': int(price),
        'available': int(available_wed_thu + available_fri)
    }
    foods.append(food)

print('Inserting foods')

for food in foods:
    new_conn.execute(
        'INSERT INTO food (name, price_kr, available)'
        'VALUES (?, ?, ?)',
        (food['name'], food['price'], food['available'])
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
        'available': int(available)
    }
    snacks.append(snack)

print('Inserting snacks')

for snack in snacks:
    new_conn.execute(
        'INSERT INTO snack (name, price_kr, available)'
        'VALUES (?, ?, ?)',
        (snack['name'], snack['price'], snack['available'])
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
        'id': id,
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
        'INSERT INTO worker (id, display_name, first_name, last_name, '
        'telephone, email, address, note, status_id) '
        'VALUES '
        '(?, ?, ?, ?, ?, ?, ?, ?,(SELECT id FROM worker_status WHERE name = ?))',
        (worker['id'], worker['display_name'], worker['first_name'],
         worker['last_name'], worker['telephone'], worker['email'],
         worker['address'], worker['note'], worker['status'])
    )

new_conn.commit()
print(f'Inserted {len(workers)} workers!')

# SHIFTS
START_DATE = '2006-01-01'
print(f'Getting shifts (starting from {START_DATE})')


old_cursor.execute(f'SELECT * FROM transactions WHERE date >= {START_DATE}')
shifts = []

type_lookup = {
    0: 'legacy shift type',
    1: 'bar',
    2: 'kitchen',
    3: 'legacy shift type',
    4: 'legacy shift type',
    5: 'legacy shift type',
    6: 'legacy shift type',
    7: 'legacy shift type',
    8: 'legacy shift type',
    9: 'legacy shift type',
    10: 'legacy shift type',
    12: 'legacy shift type',
}

for id, date_time, worker_id, shift_type, duration in old_cursor:
    start_time = date_time.time()

    delta = datetime.timedelta(hours=duration)
    dummy_datetime = datetime.datetime(
            1, 1, 1,
            hour=start_time.hour,
            minute=start_time.minute,
            second=start_time.second,
    )
    end_datetime = dummy_datetime + delta
    end_time = end_datetime.time()

    shift = {
        'id': id,
        'worker_id': int(worker_id),
        'shift_type': type_lookup[int(shift_type)],
        'date': date_time.date().isoformat(),
        'start': start_time.isoformat(),
        'end': end_time.isoformat(),
    }
    shifts.append(shift)

print('Inserting shifts')

for shift in shifts:
    new_conn.execute(
        'INSERT INTO shift (id, worker_id, date, start, end, shift_type_id) '
        'VALUES (?, ?, ?, ?, ?, (SELECT id FROM shift_type WHERE name = ?))',
        (shift['id'], shift['worker_id'], shift['date'], shift['start'],
         shift['end'], shift['shift_type'])
    )

new_conn.commit()
print(f'Inserted {len(shifts)} shifts!')
