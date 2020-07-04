import os
import unittest
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app

casting_assistant = os.environ.get('casting_assistant')
casting_director = os.environ.get('casting_director')
executive_producer = os.environ.get('executive_producer')

auth0_tokens = {
    "casting_assistant": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5N2RmOTI4ODJjMDAxMzViOGU3MiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzkwMDQ0NCwiZXhwIjoxNTkzOTg2ODQ0LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.emZpeine11R-7JgFClbVoICGCD0bN_wltRNX5E4nnOFCdL1BSU_2Wetf1MJiMiBubZ2cQA0TuFXFpzB5F-XZpg5WRf0SKhNoabM_0uL9WgwYGPnznz6RO3tNP275BGqt1_UKbh_99oO1TasWw6dNs67fF1t8ET4wjQ3U27VxTBQuaho2viqXKBMGwF1pQ0_zwcPFWUtIeLnUIrk7DPfbfUsuVNuNsuWnVVBxTzj6nDLRrwAbElQJKY9nzynOMeEwRK3siWTrT5MN-gT7Qvqj1oYcAJ-d_GZRUW74bCG5DENZw_2P_kgY1vXQuVlJlIO7jTLik35LTpNhfHOEt1LmtQ",
    "casting_director": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODBjZDQ0ZWQ4MDAxOTQ0NmZkYyIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzkwMDU4NiwiZXhwIjoxNTkzOTg2OTg2LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.KY3oudlBsYVPA4FgXmr5W86DkVqZr93MkMpQpoQfWTY6tysnixDQOrO34-9VtWwdsxpMvbh43ZfgzqbB25iVsNGQwCIS404hSnVIPjpRC40LtZnnWwBO-wDHke1DuR0xeLwSJXeYLN0cCFrGV1gzO4ZfqzsUz2h11t_WXaM-qxrvgNH6fpNUIjGm2PD3qM8cIuE7Fn8MTvNbFiiu8VSl1eafowdaaGCfdqTu4ChNBmaIoCFIxT3ZZhwDuD9ByZKOsBsPPpxH4pr3S3I2Y3nO3Iuks4cwDC33LUhiY2DzYCfk1gx4aoWHFXpZ73BhBexGua_0ukTTzIv_wHjNOEeHQg",
    "executive_producer": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODJkM2UwZGU4MDAxMzk3MDI3NiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzkwMDYyMCwiZXhwIjoxNTkzOTg3MDIwLCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.WN0WJwAIm9ifiYX9BSguz9lHx5-cbv1U4QrJpFqek7wd0VxOH8NePyWyobKNxz5AXIY7A5C4ZtsG_PgBewnOanUPfC87GhnCfhAZ2vF6qXOA72F7bDj4resEApkZ1qftmFuBvL15wH79QPt3mKcpFAc21JhyngugHCi1Kw_Hgkj6SM1bMXVwLRGfa7D6bl27gUD9inX1_UJnYiSd_h723dU5wdHxQ8-GgeahWV-OxuGvhYBnbXfUbA7xuELi6JVFlw14UIrVld-WnXzUtsPKWsdit-3a1wOOp7CHDa5faEYFhvIwTXYqYt-ZDdKofANH6-wRqRsiYltYilRNvcnTrQ"
}


def headers(token):
    response = {
        "Authorization": token
    }
    return response


class CapstoneTestCases(unittest.TestCase):
    """This class represents the capstone project test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.auth_header_executive = headers(auth0_tokens["executive_producer"])
        self.auth_casting_assistant = headers(auth0_tokens["casting_assistant"])
        self.auth_casting_director = headers(auth0_tokens["casting_director"])

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

#----------------------------------------#
# The endpoints test 1-8 are performed with the executive producer role since it has all the permissions
# Testing the other roles are performed in tests 9-12
#----------------------------------------#
# (1) successful GET endpoint tests
#----------------------------------------#

    def test_get_actors_successful(self):
        res = self.client().get('/actors', headers=self.auth_header_executive)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']))

    def test_get_movies_successful(self):
        res = self.client().get('/movies', headers=self.auth_header_executive)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']))

#----------------------------------------#
# (2) not successful GET endpoint tests
#----------------------------------------#

    def test_get_actors_not_successful(self):
        res = self.client().get('/actors/1', headers=self.auth_header_executive)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_movies_not_successful(self):
        res = self.client().get('/movies/1', headers=self.auth_header_executive)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

#----------------------------------------#
# (3) successful POST endpoint tests
#----------------------------------------#

    def test_post_actors_successful(self):
        res = self.client().post('/actors',
                                 json={
                                     'name': 'Actor 1',
                                     'age': 30,
                                     'gender': 'F'
                                 }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_post_movies_successful(self):
        res = self.client().post('/movies',
                                 json={
                                     'title': 'Movie 1',
                                     'release_date': '2020-03-01'
                                 }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

#----------------------------------------#
# (4) not successful POST endpoint tests
#----------------------------------------#

    def test_post_actors_not_successful(self):
        res = self.client().post('/actors',
                                 json={
                                     'name': 'Actor 1',
                                     'age': "invalid age",
                                     'gender': 'F'
                                 }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_post_movies_not_successful(self):
        res = self.client().post('/movies',
                                 json={
                                     'title': 'Movie 1',
                                     'release_date': 'invalid date'
                                 }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#----------------------------------------#
# (5) successful PATCH endpoint tests
#----------------------------------------#

    def test_patch_actors_successful(self):
        res = self.client().patch('/actors/3',
                                  json={
                                      'name': 'Actor 5',
                                      'age': 35,
                                      'gender': 'M'
                                  }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_patch_movies_successful(self):
        res = self.client().patch('/movies/3',
                                  json={
                                      'title': 'Movie 5',
                                      'release_date': '2015-03-01'
                                  }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

#----------------------------------------#
# (6) not successful PATCH endpoint tests
#----------------------------------------#

    def test_patch_actors_not_successful(self):
        res = self.client().patch('/actors/3',
                                  json={
                                      'name': 'Actor 5',
                                      'age': "invalid age",
                                      'gender': 'M'
                                  }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch_movies_not_successful(self):
        res = self.client().patch('/movies/3',
                                  json={
                                      'title': 'Movie 5',
                                      'release_date': 'invalid date'
                                  }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#----------------------------------------#
# (7) successful DELETE endpoint tests
# Note: the id must be updated to an existing id 
#----------------------------------------#

    def test_delete_actor_successful(self):
        res = self.client().delete('/actors/3', headers=self.auth_header_executive)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(actor, None)

    def test_delete_movie_successful(self):
        res = self.client().delete('/movies/3', headers=self.auth_header_executive)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(movie, None)

#----------------------------------------#
# (8) not successful DELETE endpoint tests
#----------------------------------------#

    def test_delete_actor_not_successful(self):
        res = self.client().delete('/actors/500', headers=self.auth_header_executive)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 500).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_movie_not_successful(self):
        res = self.client().delete('/movies/500', headers=self.auth_header_executive)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 500).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------#
# (9) successful GET endpoint tests with Role casting assistant
#----------------------------------------#

    def test_get_actors_successful_casting_assistant(self):
        res = self.client().get('/actors', headers=self.auth_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']))

    def test_get_movies_successful_casting_assistant(self):
        res = self.client().get('/movies', headers=self.auth_casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']))

#----------------------------------------#
# (10) not successful POST endpoint tests with Role casting assistant
#----------------------------------------#

    def test_post_actors_not_successful_casting_assistant(self):
        res = self.client().post('/actors',
                                 json={
                                     'name': 'Actor 1',
                                     'age': 30,
                                     'gender': 'F'
                                 }, headers=self.auth_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------#
# (12) successful GET endpoint tests with Role casting director
#----------------------------------------#

    def test_get_actors_successful_casting_director(self):
        res = self.client().get('/actors', headers=self.auth_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']))

    def test_get_movies_successful_casting_director(self):
        res = self.client().get('/movies', headers=self.auth_casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']))


#----------------------------------------#
# (12) successful POST acotr endpoint tests with Role casting director
#----------------------------------------#


    def test_post_actors_successful_casting_director(self):
        res = self.client().post('/actors',
                                 json={
                                     'name': 'Actor 1',
                                     'age': 30,
                                     'gender': 'F'
                                 }, headers=self.auth_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']))

#----------------------------------------#
# (12) not successful POST movie endpoint tests with Role casting director
#----------------------------------------#

    def test_post_movies_not_successful_casting_director(self):
        res = self.client().post('/movies',
                                 json={
                                     'title': 'Movie 1',
                                     'release_date': '2020-03-01'
                                 }, headers=self.auth_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


#----------------------------------------#
# END of tests
#----------------------------------------#
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
