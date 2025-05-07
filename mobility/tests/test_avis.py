# veuillez utilisez cette commande dans le terminal pour lancer les test 
#   -->  python3 -m unittest discover -v -s ./mobility/tests

import unittest
import tempfile
import os
from mobility import create_app
from mobility.db import get_db, close_db
from mobility.models.avis import inserer_avis

class AvisTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = get_db()
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def test_inserer_avis(self):
        # Insertion d'un avis
        inserer_avis("Alice", "Bon service", "Très satisfaite du vol", 4, "alice.jpg")

        # Vérification dans la base
        avis = self.db.execute("""
            SELECT prenom, entete, message, note, photo_profil FROM avis
        """).fetchone()

        self.assertIsNotNone(avis)
        self.assertEqual(avis[0], "Alice")
        self.assertEqual(avis[1], "Bon service")
        self.assertEqual(avis[2], "Très satisfaite du vol")
        self.assertEqual(avis[3], 4)
        self.assertEqual(avis[4], "alice.jpg")
    def tearDown(self):
        # closing the db and cleaning the temp file
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)