import sqlite3
from flask import current_app, g

def get_db():
    """Returns the database connection. Create the connection if needed.

    Returns:
        db: The db connection to be used for SQL functions
    """

    # g is the shorthand for "globals" and allows registering available in the whole Flask app
    if 'db' not in g:
        # If it's not there, let's create the db connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        print(current_app.config['DATABASE'])

        # Instead of getting "tuple" out of queries, we'll get dictionaries of column->value
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Close the database

    Args:
        e: unused
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_db():
    db = get_db()
    # Not necessary for the project
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    app.teardown_appcontext(close_db)