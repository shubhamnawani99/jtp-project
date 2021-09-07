from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .db import get_db

bp = Blueprint('recommendation', __name__)


# end point "index" as defined using add_url_rule in __init__
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT book_id, authors, title from books'
    ).fetchall()

    return render_template('recommendation-system/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # the call to recommender system goes here...
            print(title, body)
            return redirect(url_for('recommendation.index'))

    return render_template('recommendation-system/create.html')
