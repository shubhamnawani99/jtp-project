import os
from flask import Flask, render_template

'''
    Custom error pages
'''


# page not found error
def page_not_found(e):
    return render_template('404.html'), 404


# internal server error
def internal_server_error(e):
    return render_template('500.html'), 500


# "__init__.py" identifies book-recommender-system as package
# Application factory created for scaling
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # define your database here
        DATABASE=os.path.join(app.instance_path, 'book-RecSys.db'),
        SEARCH_URL='https://yandex.com/images/search',
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'},
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

    try:
        os.makedirs(os.path.join(app.instance_path, 'htmlfi'))
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import controller
    app.register_blueprint(controller.bp)
    app.add_url_rule('/', endpoint='index')

    return app
