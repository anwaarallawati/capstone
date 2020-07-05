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

AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL')


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
        self.auth_header_executive = headers(executive_producer)
        self.auth_casting_assistant = headers(casting_assistant)
        self.auth_casting_director = headers(casting_director)

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
