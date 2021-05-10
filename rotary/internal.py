from flask import Blueprint, g, render_template, request, session
from datetime import date, timedelta

from rotary.db import get_db
from rotary.auth import login_required

bp = Blueprint('internal', __name__, url_prefix='/internal')


@bp.route('/')
@login_required
def index():
    return render_template('internal/index.html')
