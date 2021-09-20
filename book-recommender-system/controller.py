# import the necessary libraries and methods
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash, current_app
)

from .db import get_db
from .recommender import main
from .user_selections import UserSelection
from .reverse_search_engine import get_url, get_keywords_from_img, get_book_title_from_keywords

# register the blueprint name
bp = Blueprint('controller', __name__)

# create the user selection object
# this object will hold all the books and ratings selected by the user
user_selection = UserSelection()


# end point "index" as defined using add_url_rule in __init__
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':

        # fill the current user selections with book title and ratings
        if 'select-form' in request.form:
            book_selected = request.form.get("book-choice")
            rating_selected = request.form.get("book-rating")
            user_selection.set_user_selection(book_title=book_selected, book_rating=rating_selected)

        # process the form
        elif 'process-form' in request.form:
            # send user selections to the recommender system and get recommendations
            user, filtered = main(user_selection.get_user_selection())
            # clear the selections
            # user_selection.clear_selections()
            return render_template('recommendation-system/output.html', user_result=user, filter_result=filtered)

    # load the book list into the "select input" from the database
    db = get_db()
    books = db.execute(
        'SELECT distinct book_id, authors, title, image_url from books limit 10'
    ).fetchall()

    # render the index template
    return render_template('recommendation-system/index.html', books=books,
                           current_list=user_selection.get_user_selection(),
                           length=user_selection.get_length())


# Clear all selections both book titles and ratings
@bp.route('/clear')
def clear_selections():
    user_selection.clear_selections()
    return redirect(url_for('controller.index'))


# Delete a particular selection
@bp.route('/delete', methods=['POST'])
def delete():
    # get the book name
    key = request.form.get('del-item')
    # delete the book title (key) and the corresponding rating from the dictionary
    user_selection.del_selection(key)
    # return to the homepage
    return redirect(url_for('controller.index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/image_recognition', methods=['GET', 'POST'])
def image_recognition():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # get the uploaded file
        f = request.files['file']
        # if user does not select file, browser also
        # submits an empty part without filename
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # get the URL for the reverse search result
        if f and allowed_file(f.filename):
            response = get_url(f)
            # get the keywords from the image
            keywords = get_keywords_from_img(response)

            # get the book details
            # keywords = ['k.', 'd.', 'garri', 'roling', 'rosmen', 'kniga', 'potter', "kamen'", 'oblozhki']
            details = get_book_title_from_keywords(keywords)
            return render_template('recommendation-system/choose_book.html', books=details)
        flash('Invalid file-extension')
    return render_template('recommendation-system/image_rec.html')
