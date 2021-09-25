"""Database module to set up the database"""
import sqlite3

from flask import current_app, g


def get_db():
    """
    :return: the database instance
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e):
    """Close the database"""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """tells Flask to call that function when cleaning up after returning the response.

    :param app: Flask app instance
    """
    app.teardown_appcontext(close_db)
