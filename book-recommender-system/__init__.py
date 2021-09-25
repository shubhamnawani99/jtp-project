""""__init__.py" identifies book-recommender-system as package"""
import os

from flask import Flask, render_template


def page_not_found(e):
    """Custom page not found error

    This method gets triggered whenever a user tries to access a page that does not exist on the server. For example:
    http://localhost:5000/this-page-does-not-exist

    :return 404.html: Page not found custom HTML page
    """
    return render_template('404.html'), 404


def internal_server_error(e):
    """Custom internal server error error

     This method gets triggered whenever an internal server error occurs

     :return 500.html: Internal server error custom HTML page
     """
    return render_template('500.html'), 500


def create_app(test_config=None):
    """Application factory created for scaling. Create a flask app instance

    :param test_config: configuration if testing is done
    :return: flask app instance
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app configurations goes here
    app.config.from_mapping(
        SECRET_KEY='dev',
        # define your database here
        DATABASE=os.path.join(app.instance_path, 'book-RecSys.db'),
        # search URL goes here
        SEARCH_URL='https://yandex.com/images/search',
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'},
        # user selection limit goes here
        USER_SELECTION_LIMIT=5,
    )

    # register the app handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ensure the html files folder exists
    try:
        os.makedirs(os.path.join(app.instance_path, 'htmlfi'))
    except OSError:
        pass

    from . import db
    # initialize the database
    db.init_app(app)

    from . import controller
    # register the controller
    app.register_blueprint(controller.bp)
    app.add_url_rule('/', endpoint='index')

    return app
