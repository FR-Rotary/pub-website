import mysql.connector

from flask import current_app, g


def exec_mariadb(query: str):
    db_config = {
        'host': current_app.config['MARIADB_HOST'],
        'user': current_app.config['MARIADB_USER'],
        'password': current_app.config['MARIADB_PASS'],
        'database': current_app.config['MARIADB_DB'],
    }
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result
