from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from .db import get_db
from .recommender import main

bp = Blueprint('recommendation', __name__)

current_list = dict()


# end point "index" as defined using add_url_rule in __init__
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':

        # fill the current dictionary with book title and ratings
        if 'select-form' in request.form:

            books_selected = request.form.getlist("book-choice")
            book_ratings = request.form.get("book-rating")

            for book, rating in zip(books_selected, book_ratings):
                current_list[book] = int(rating)

        # process the form
        elif 'process-form' in request.form:

            result = main(current_list)
            current_list.clear()

            return render_template('recommendation-system/process.html', result=result)

    # load the book list into the select input from the database
    db = get_db()
    books = db.execute(
        'SELECT book_id, authors, title from books limit 10'
    ).fetchall()

    length = len(current_list) | 0

    # render the index template
    return render_template('recommendation-system/index.html', books=books, current_list=current_list,length=length)


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
            return redirect(url_for('recommendation.index'))

    return render_template('recommendation-system/create.html')
