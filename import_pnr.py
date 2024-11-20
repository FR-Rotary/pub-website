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


# WORKERS
old_cursor.close()
old_conn.close()
old_conn = mysql.connector.connect(**db_credentials, database='tidslista')
old_cursor = old_conn.cursor()

print('Connected to workers & hours DB')
print('Getting workers')

old_cursor.execute('SELECT * FROM users')
workers = []

for id, name, first_name, last_name, phone, mobile, ip, email, status, personal_number, address, note in old_cursor:
    worker = {
        'id': id,
        'pnr': personal_number if personal_number else "-1",
    }
    workers.append(worker)

print('Updating workers')

for worker in workers:
    new_conn.execute(
        'UPDATE worker '
        'SET personal_id_number = ? '
        'WHERE id = ?',
        (worker['pnr'], worker['id'])
    )

new_conn.commit()
print(f'Updated {len(workers)} workers!')

