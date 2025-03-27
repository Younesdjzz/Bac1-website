import tempfile
import unittest
import os

from mobility import create_app
from mobility.db import get_db, close_db
from mobility.models.airport import (
    get_all_airports,
    search_airport_by_iata_code,
    nombre_de_vols_par_type,
    nombre_de_vols_par_jour,
    Airport
)

class AirportTestCase(unittest.TestCase):
    def setUp(self):

        # generate a temporary file for the test db
        self.db_fd, self.db_path = tempfile.mkstemp()
        # create the testapp with the temp file for the test db
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = get_db()
        # read in SQL for populating test data
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def test_get_all_airports(self):
        names=get_all_airports()
        airport=[r[0] for r in names]
        self.assertIn("Charles de Gaulle", airport)
        self.assertIn("Brussels-South Charleroi", airport)

    def test_search_airport_by_iata_code(self):
        result = search_airport_by_iata_code("CDG")[0]    
        self.assertEqual(result[1:],("Charles de Gaulle", 49.0097, 2.5479, "FR"))
        result = search_airport_by_iata_code("CRL")[0]    
        self.assertEqual(result[1:],("Brussels-South Charleroi", 60, 70, "BE"))
        

    def test_nombre_de_vols_par_type(self):
        result = nombre_de_vols_par_type("CDG")
        types = [r[0] for r in result]  # r[0] = aircraft_type
        self.assertIn("Jet", types)

    def test_nombre_de_vols_par_jour(self):
        result = nombre_de_vols_par_jour("CDG")
        self.assertEqual(len(result), 1)  # ← le test est maintenant logique

    def test_airport_get(self):
        airport = Airport.get("CDG")
        self.assertIsNotNone(airport)
        self.assertEqual(airport.name, "Charles de Gaulle")
        self.assertEqual(airport.iso_country, "FR")

    def tearDown(self):
        # closing the db and cleaning the temp file
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)