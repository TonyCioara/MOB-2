import app2
import unittest
import json
from pymongo import MongoClient

db = None

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app2.app.test_client()

        # Run app in testing mode to retrieve exceptions and stack traces
        app2.app.config['TESTING'] = True

        # Inject test database into application
        mongo = MongoClient('localhost', 27017)
        global db
        db = mongo.test_database
        app2.app.db = db

        ## We do this to clear our database before each test runs
        db.drop_collection('trips')

    def test_getting_a_trip(self):

        ## Post 2 users to database
        # post_restult =
        self.app.post('/trips',
                          headers=None,
                          data=json.dumps(dict(
                              destination="Germany",
                              trip_day_amount=7
                          )),
                          content_type='application/json')

        ## 3 Make a get request to fetch the posted user

        response = self.app.get('/trips',
                                query_string=dict(destination="Germany")
                            )

        # Decode reponse
        response_json = json.loads(response.data.decode())

        ## Actual test to see if GET request was succesful
        ## Here we check the status code
        self.assertEqual(response.status_code, 200)

    def test_patching_a_trip(self):

        ## Post 2 users to database
        self.app.post('/trips',
                          headers=None,
                          data=json.dumps(dict(
                              destination="Germany",
                              trip_day_amount=7
                          )),
                          content_type='application/json')

        ## 3 Make a get request to fetch the posted user

        response = self.app.patch('/trips',
                                query_string=dict(destination="Germany"),
                                data=json.dumps(dict(
                                    destination="SaN FRAN",
                                )),
                                content_type='application/json')

        # Decode reponse
        response_json = json.loads(response.data.decode())

        ## Actual test to see if GET request was succesful
        ## Here we check the status code
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
