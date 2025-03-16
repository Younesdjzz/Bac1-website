import sqlite3
import os
from flask import current_app, g

def get_db():
    """Returns the database connection. Create the connection if needed.

    Returns:
        db: The db connection to be used for SQL functions
    """
    # g is the shorthand for "globals" and allows registering available in the whole Flask app
    if 'db' not in g:
        # Create the database connection if not already present
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        print(current_app.config['DATABASE'])  # Debug print to see the database path

        # Use dictionaries instead of tuples for the result of queries
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialise la base de données en exécutant le script de schéma si la base n'existe pas déjà."""
    db = get_db()
    # Vérifier si la base de données existe déjà pour ne pas la recréer
    if not os.path.exists(current_app.config['DATABASE']):
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

def init_app(app):
    """Set up the app context for closing the database connection."""
    app.teardown_appcontext(close_db)
