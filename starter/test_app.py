import os
import unittest
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app

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
# (1) successful GET endpoint tests
#----------------------------------------# 

    def test_get_actors_successful(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']))

    def test_get_movies_successful(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']))

#----------------------------------------# 
# (2) not successful GET endpoint tests
#----------------------------------------# 

    def test_get_actors_not_successful(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_movies_not_successful(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

#----------------------------------------# 
# (3) successful POST endpoint tests
#----------------------------------------# 

    def test_post_actors_successful(self):
        res = self.client().post('/actors',
            json={
                'name' : 'Actor 1',
                'age' : 30,
                'gender' : 'F'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_post_movies_successful(self):
        res = self.client().post('/movies',
            json={
                'title' : 'Movie 1',
                'release_date' : '2020-03-01'
                })
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
                'name' : 'Actor 1',
                'age' : "invalid age",
                'gender' : 'F'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_post_movies_not_successful(self):
        res = self.client().post('/movies',
            json={
                'title' : 'Movie 1',
                'release_date' : 'invalid date'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#----------------------------------------# 
# (5) successful PATCH endpoint tests
#----------------------------------------# 

    def test_patch_actors_successful(self):
        res = self.client().patch('/actors/3',
            json={
                'name' : 'Actor 5',
                'age' : 35,
                'gender' : 'M'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_patch_movies_successful(self):
        res = self.client().patch('/movies/3',
            json={
                'title' : 'Movie 5',
                'release_date' : '2015-03-01'
                })
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
                'name' : 'Actor 5',
                'age' : "invalid age",
                'gender' : 'M'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch_movies_not_successful(self):
        res = self.client().patch('/movies/3',
            json={
                'title' : 'Movie 5',
                'release_date' : 'invalid date'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#----------------------------------------# 
# (7) successful DELETE endpoint tests
#----------------------------------------#     

    def test_delete_actor_successful(self):
        res = self.client().delete('/actors/5')
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(actor, None)

    def test_delete_movie_successful(self):
        res = self.client().delete('/movies/5')
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(movie, None)

#----------------------------------------# 
# (8) not successful DELETE endpoint tests
#----------------------------------------#   

    def test_delete_actor_not_successful(self):
        res = self.client().delete('/actors/500')
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 500).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_movie_not_successful(self):
        res = self.client().delete('/movies/500')
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 500).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------#  
# END of tests 
#----------------------------------------#      
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
