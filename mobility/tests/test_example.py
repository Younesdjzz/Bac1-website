# import os
# import tempfile
# import unittest
# import json

# from mobility import create_app
# from mobility.db import close_db, get_db
# from mobility.models.airport import search_airport_by_iata_code


# class TestUser(unittest.TestCase):
#     def test_country_list(self):
#         # unit test against the test db.
#         expected_countries = [
#             {"iso_country": "FI", "name": "Finland"},
#             {"iso_country": "FR", "name": "France"}
#         ]
#         # easy way to convert sqlite3.Row to dict
#         actual_countries = [dict(row) for row in search_airport_by_iata_code()]
#         self.assertEqual(len(actual_countries), 2)
#         for i in range(len(expected_countries)):
#             actual_country = actual_countries[i]
#             expected_country = expected_countries[i]
#             self.assertEqual(actual_country, expected_country)

#     def setUp(self):

#         # generate a temporary file for the test db
#         self.db_fd, self.db_path = tempfile.mkstemp()
#         # create the testapp with the temp file for the test db
#         self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
#         self.app_context = self.app.app_context()
#         self.app_context.push()

#         self.db = get_db()
#         # read in SQL for populating test data
#         with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
#             self.db.executescript(f.read().decode("utf8"))

#     def tearDown(self):
#         # closing the db and cleaning the temp file
#         close_db()
#         os.close(self.db_fd)
#         os.unlink(self.db_path)