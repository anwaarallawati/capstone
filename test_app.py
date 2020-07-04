import os
import unittest
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app


auth0_tokens = {
    "casting_assistant": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5N2RmOTI4ODJjMDAxMzViOGU3MiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzgyMDUzNywiZXhwIjoxNTkzOTA2OTM3LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.DCXRN9E4iHHi2Z_BV7pRrHwCDX10mqW5Zx4U8DOaTiDHqKAkJrNpUYEJAUYqR7NB7EuR0iWTNEOd3c-J7EseF-cH5VWFLxhuGUHYAkqIj3d9clRqJXqQdD0MVwMb0hYg45UJEDVKHyqlAXSaMKvxrv7q_mVRlomhD6Cx0vD7ayHfonUeiYHqQpdimxJtD448g1yWFStW8V2S15wfIYNPqZt_45YNBdyKvPkWV-s4cKNQd1KTNvzHYBXgRae19S4ZTyoTWH_jH1aTc8x1IJoJZ-pNgV9VJaV-0OnBmvm6MnNtUI9XnXWsMxpTMNVwCtcSi6QWVCGLKA0Uumny_cZ76g",
    "casting_director": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODBjZDQ0ZWQ4MDAxOTQ0NmZkYyIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzgyMDU3OCwiZXhwIjoxNTkzOTA2OTc4LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.BW7-_dItx0i0nfTukzdMNfEG6pH8NA0Abo_oZ-nrhVtfvU0HAswz6RpufPqPbs7Ug0-ui_snSxxlTpuAreJ5NQF70qcmYgri2MNsucF5jQr_agAU7VkB6mIcKgh5n4Earb5P6ZsAsKEK16aFubVPo7Ty0uh5LQZH6yd_KUbbbLqovtaiorZC04WzeyiLoni9rutsc1jS6Z02-_jEHCn4lyzx9s8heuX8cBO5f7U_dN_3qb8-VcU9Zi8RZzzLwHPMEPABo9VlTXdJPaaKmILeRELXXH7J51RXslu6E8FW1JLXQbYVYPMjUuwnQ7H2Ahbdi2IylXMfaZ3XMixViv-dNQ",
    "executive_producer": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODJkM2UwZGU4MDAxMzk3MDI3NiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzgyMDYxNSwiZXhwIjoxNTkzOTA3MDE1LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.d3hDGIoUPIZ9s65m7tzOJm5n4fblCAMnpqEH8Qr_-3nals4H9hf_DKgyj0_dFbKZeKMT0LJmTPeR__U23UbIi-UEe0Tug7KXk_Mc373VXWMJ20-q7nTdRafG3gxw5ctO5j8u61-eFGvlrHUukKImnAd_rr2bHIz0HNs3mio9ZAtJNcqbxvpTl3-3-YccsHpjukjHRVpMgad710RHWFXfvGNY91plxdiYT3inpksrIovlmgV91dlVlnkJELamA08QUxkIckKt4HdWHhan5YHqFWaWUrRKWPuHaQuXZfF6RfAvrWDZcU40ns_321VbCvK45CbS6e80Mqk5Qe23yFyGpA"
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
#----------------------------------------#

    def test_delete_actor_successful(self):
        res = self.client().delete('/actors/5', headers=self.auth_header_executive)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(actor, None)

    def test_delete_movie_successful(self):
        res = self.client().delete('/movies/5', headers=self.auth_header_executive)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 5).one_or_none()

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
