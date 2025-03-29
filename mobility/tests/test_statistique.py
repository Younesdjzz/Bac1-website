import tempfile
import unittest
import os

from mobility import create_app
from mobility.db import get_db, close_db
from mobility.models.stats import (
    number_data_airline,
    number_data_airport,
    number_data_country,
    number_data_aircraft,
    number_data_flight

)


class TestUser(unittest.TestCase):

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
    
    def test_number_data_airline(self):
        total_airlines, airlines_flight_count = number_data_airline()

        
        self.assertEqual(total_airlines, 2)


        expected_counts = {
            "Air France": 1, 
            "Finnair": 1
        }
        self.assertEqual(airlines_flight_count, expected_counts)
    def test_number_data_airport(self):
        total_airports = number_data_airport()
        self.assertEqual(total_airports, 2)
    def test_number_data_country(self):
        total_countries = number_data_country()
        self.assertEqual(total_countries, 2)  

    def test_number_data_aircraft(self):
        total_aircraft=number_data_aircraft()
        self.assertEqual(total_aircraft,2)
    
    def test_number_data_flight(self):
        total_flight, flights_per_airport = number_data_flight()
        self.assertEqual(total_flight, 2)
        expected_counts = {
            "Charles de Gaulle": 1,
            "Brussels-South Charleroi": 1
        }
        self.assertEqual(flights_per_airport, expected_counts)
    def tearDown(self):
        # closing the db and cleaning the temp file
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)