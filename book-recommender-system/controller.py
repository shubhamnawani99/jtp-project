# import the necessary libraries and methods
import requests.exceptions
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash, current_app,
)

from .db import get_db
from .recommender import book_recommender_system
from .reverse_search_engine import get_url, get_keywords_from_img, get_book_title_from_keywords
from .user_selections import UserSelection

# register the blueprint name
bp = Blueprint('controller', __name__)

# create the user selection object
# this object will hold all the books and ratings selected by the user
user_selection = UserSelection()


@bp.app_template_global()
def selection_limit() -> bool:
    return user_selection.get_length() < current_app.config['USER_SELECTION_LIMIT']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# end point "index" as defined using add_url_rule in __init__
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':

        # fill the current user selections with book title and ratings
        if 'select-form' in request.form:
            book_selected = request.form.get("book-choice")
            rating_selected = request.form.get("book-rating")
            user_selection.set_user_selection(book_title=book_selected, book_rating=rating_selected)
            print(book_selected)
        # process the form
        elif 'process-form' in request.form:
            if user_selection.not_null():
                # send user selections to the recommender system and get recommendations
                user, filtered = book_recommender_system(user_selection.get_user_selection())
                if len(user) == 0:
                    flash('Sorry we have no recommendation for the user selections in our database. \
                    Please try again with other books and ratings')
                    return redirect(request.url)
                # clear the selections
                user_selection.clear_selections()
                return render_template('recommendation-system/output.html', user_result=user, filter_result=filtered)

    # load the book list into the "select input" from the database
    db = get_db()
    books = db.execute(
        'SELECT distinct book_id, authors, title, image_url from books limit 2500'
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
        # if file is correct
        if f and allowed_file(f.filename):
            # get the URL for the reverse search result
            try:
                response = get_url(f)
                # get the keywords from the image
                keywords = get_keywords_from_img(response)
                # get the book details
                details = get_book_title_from_keywords(keywords)
                if len(details) == 0:
                    flash('No titles available for the given image. Please try with a different book cover')
                    return redirect(request.url)
                return render_template('recommendation-system/choose_book.html', books=details)
            except requests.exceptions.ConnectionError:
                flash('The reverse image service has reached the query limit')
                return redirect(request.url)

        flash('Invalid file-extension')

    # deny access to image recognition if the user has selected all 5 books
    if user_selection.get_length() >= 5:
        return redirect(url_for('controller.index'))

    return render_template('recommendation-system/image_rec.html')
