from flask import Blueprint, g, render_template, request, session
from datetime import date, timedelta

from rotary.db import get_db

bp = Blueprint('internal', __name__, url_prefix='/internal',
               template_folder='templates/external')


@bp.route('/')
def index():
    return render_template('internal/index.html')
