from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from .db import get_db
from .recommender import main

bp = Blueprint('controller', __name__)

# current_list = dict()
# testing list
current_list = {'The Hunger Games (The Hunger Games, #1)': 1,
                "Harry Potter and the Sorcerer's Stone (Harry Potter, #1)": 2, 'To Kill a Mockingbird': 3,
                'The Fault in Our Stars': 1, 'The Hobbit': 5}


# end point "index" as defined using add_url_rule in __init__
@bp.route('/', methods=('GET', 'POST'))
def index():
    print(current_list)
    if request.method == 'POST':

        # fill the current dictionary with book title and ratings
        if 'select-form' in request.form:

            books_selected = request.form.getlist("book-choice")
            book_ratings = request.form.get("book-rating")

            for book, rating in zip(books_selected, book_ratings):
                current_list[book] = int(rating)

        # process the form
        elif 'process-form' in request.form:

            # clear the dictionary
            result = main(current_list)
            # current_list.clear()

            return render_template('recommendation-system/output.html', result=result)

    # load the book list into the select input from the database
    db = get_db()
    books = db.execute(
        'SELECT book_id, authors, title, image_url from books limit 10'
    ).fetchall()

    length = len(current_list) | 0

    # render the index template
    return render_template('recommendation-system/index.html', books=books, current_list=current_list, length=length)


# Clear all selections both book titles and ratings
@bp.route('/clear')
def clear_selections():
    # current_list.clear()
    return redirect(url_for('controller.index'))


# Delete a particular selection
@bp.route('/delete', methods=['POST'])
def delete():
    # get the book name
    key = request.form.get('del-item')
    # delete the book title (key) and the corresponding rating from the dictionary
    current_list.pop(key)
    # return to the homepage
    return redirect(url_for('controller.index'))

