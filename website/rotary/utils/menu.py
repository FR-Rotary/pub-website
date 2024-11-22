import os
import subprocess
from tempfile import TemporaryDirectory

from flask import Response

from rotary.db import get_db

def generate_pdf(tex_content, output_filename='texput.pdf'):
    with TemporaryDirectory() as tmpdir:
        try:
            result = subprocess.run(
                ['pdflatex', '-halt-on-error', '-output-directory', tmpdir],
                input=tex_content.encode('utf8'),
                capture_output=True,
                check=True,
                timeout=10,
            )
            pdf_path = os.path.join(tmpdir, output_filename)
            with open(pdf_path, 'rb') as pdf:
                return Response(pdf.read(), mimetype='application/pdf')
        except subprocess.CalledProcessError as e:
            return Response(
                f"Error: {e.stderr.decode('utf8')}",
                mimetype='text/plain'
            )
        except subprocess.TimeoutExpired as e:
            return Response(
                f"Timeout: {e.stderr.decode('utf8')}",
                mimetype='text/plain'
            )
        
def fetch_menu_data():
    db = get_db()
    category_names = db.execute(
        'SELECT id, name_sv AS name FROM beer_category ORDER BY priority ASC'
    ).fetchall()

    categories = []
    for category_name in category_names:
        query = (
            'SELECT beer.name as name, style, beer_category.name_sv as category, '
            'country_iso_3166_id as country_code, abv, volume_ml, price_kr '
            'FROM beer INNER JOIN beer_category '
            'ON beer.category_id = beer_category.id '
            'WHERE available = 1 AND beer_category.id = ?'
        )
        category = {
            'name': category_name["name"],
            'beers': db.execute(query, (category_name["id"],)).fetchall()
        }
        categories.append(category)

    foods = db.execute('SELECT * FROM food WHERE available = 1 ORDER BY name ASC').fetchall()
    snacks = db.execute('SELECT * FROM snack WHERE available = 1 ORDER BY name ASC').fetchall()

    return categories, foods, snacks