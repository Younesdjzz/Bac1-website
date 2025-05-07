# veuillez utilisez cette commande dans le terminal pour lancer les test 
#   -->  python3 -m unittest discover -v -s ./mobility/tests

import unittest
import tempfile
import os
from mobility import create_app
from mobility.db import get_db, close_db
from mobility.models.graph import aeroport_bel_info,flight_world_info

class AeroportBelInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = get_db()
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def test_aeroport_bel_info_crl(self):
        with self.app.app_context():
            vols = aeroport_bel_info("CRL")

        self.assertEqual(len(vols), 1)

        vol = vols[0]
        self.assertEqual(vol["aeroport_dep"], "Brussels-South Charleroi")
        self.assertEqual(vol["Aeroport_arr"], "Charles de Gaulle")
        self.assertEqual(vol["Type_app"], "Jet")
        self.assertEqual(vol["lat_dep"], 50.4594)
        self.assertEqual(vol["lon_dep"], 4.4539)
        self.assertEqual(vol["Lat_arr"], 49.0097)
        self.assertEqual(vol["Lon_arr"], 2.5479)

    def tearDown(self):
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)



class FlightWorldInfoTestCase (unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = get_db()
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))


    def test_vols_trouves(self):


        with self.app.app_context():
            resultats = flight_world_info("Brussels Airport", "2024-01-01", "2024-01-31")
            self.assertIsInstance(resultats, list)
            self.assertTrue(len(resultats) > 0)
            for vol in resultats:
                
                vol_dict = dict(vol)
                self.assertIn("dep_airport_name", vol_dict)
                self.assertIn("arr_airport_name", vol_dict)
                self.assertIn("date", vol_dict)
                self.assertIn("type_app", vol_dict)

    def test_aucun_vol(self):
        with self.app.app_context():
            resultats = flight_world_info("Inexistant Airport", "1990-01-01", "1990-01-31")
            self.assertEqual(resultats, [])

    def tearDown(self):
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)
