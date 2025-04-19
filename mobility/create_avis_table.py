import sqlite3
import os

# Chemin vers ta base principale
db_path = os.path.join(os.path.dirname(__file__), '../instance/db.sqlite')

# Définition de la requête de création
create_table_query = """
CREATE TABLE IF NOT EXISTS avis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prenom TEXT NOT NULL,
    entete TEXT NOT NULL,
    message TEXT NOT NULL,
    note INTEGER NOT NULL,  -- Assurez-vous que c'est un INTEGER
    photo_profil TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""



