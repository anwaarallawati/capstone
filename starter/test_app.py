import os
import unittest
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app

auth0_users = {
    'casting_assistant@gmail.com': 'pass1234!',
    'casting_director@gmail.com': 'pass1234!',
    'executive_producer@gmail.com': 'pass1234!'
}

auth0_tokens = {
    "casting_assistant" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5N2RmOTI4ODJjMDAxMzViOGU3MiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzgxMzA0MCwiZXhwIjoxNTkzODIwMjQwLCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.et3g2E9Z9vDK0066ranWHZajDIPwvKxKl4sIjta7ait4i8pihGziXMwSG3Oxt7Q9jlzBFBciXV3NrZFE4WENROViIw0qIQzNBqZOZ1oWlzLalX1JIeiQCVunLCJsuqnY4sxVPS10PWnbiEposZqZopDUuGM52zJ7_2Ro8SIjeGQIovHQJ7UTBfkavpcvgqutaeT2LgW0fRL9t8HS5CohtX-Pa7lYu2g-xVfc6p6GhWft5DuuDNHdLseVyQ1iPNGTthSBlJ0e6XfYTz3N9rP5xl41XYVg8EEK5cTVFkfgMJoVKxNHIsDoFGxejD6D4K1cHHNLCJ_BmqiCsdkCGOgZdw",
    "casting_director" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODBjZDQ0ZWQ4MDAxOTQ0NmZkYyIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzgxMjk3NywiZXhwIjoxNTkzODIwMTc3LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.m6-zzw_HPcG5f2-aCJXYbzdsv4wwx11eboKi8A_jIN19RI1fgeRsiFL1mWoXhA-IQHgxhcFcykL-Pn76gaxb7misc9WV_17_XSR0-2tnypDM1yvF4m521nirZadza_ZVVN_pxGcBDoHDuqCEE0QITHIJfZW3SOAhqQrw1o2plHO0ry63S_L5wd3mVdHsEMfZAceBxuGwYfd8-UoAxIDBKDr1350kMxAwr9-RAWI2YPQYerVHdhzG90762wMgEq6VoqxS94TxsPJv9x6kq6KYbtoEagaiEHu0Wg06ZtuVnRUOq5Kq5821IGlbPAGoiE00qTGaB8neynCiA5y7Tnk4Nw",
    "executive_producer" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1WZWtoZHdpMFRTb2NTWC1rcUNKWiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hbnctOTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmY5ODJkM2UwZGU4MDAxMzk3MDI3NiIsImF1ZCI6ImNhcHN0b25lX2FwaSIsImlhdCI6MTU5MzgxMDc3NiwiZXhwIjoxNTkzODE3OTc2LCJhenAiOiIwcVRCdjdkTGgxYUJiV1JFcFAxQ2t4QkhHMmswMHRaNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.u5fEOZYxfW9BbCXGzztbqUIVBWMhJP-xFHLV8ly9yFO1VbQxZ-P22AsniqderIo7wlPmx3DxncwvwW-JiOvYmM8GJuaab8mlriDbcUxlm_hgE07hbGCIDN1xC4Q8s2C_lQNpzxlyRRsBODKvSBMkWj8GgOXhdFQrugHEO8SK_LnYw94UxWc-FL3_bQSo-hqWX8W266rfmx6Z2VpKcVPoknNlBewVlQQ43PpW9o6czHmqWE_3C7nHBkYeGSTlKLVIZrfHA5IDtAiPawx1_wWJK4vBSaE9CN2k_pBw8VdaV3H4x5gqrcjiIBk80Qh4o1lWPGRg2pSuA8YWPoGvVqVbdA" 
}

def headers(token) :
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
                'name' : 'Actor 1',
                'age' : 30,
                'gender' : 'F'
                }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_post_movies_successful(self):
        res = self.client().post('/movies',
            json={
                'title' : 'Movie 1',
                'release_date' : '2020-03-01'
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
                'name' : 'Actor 1',
                'age' : "invalid age",
                'gender' : 'F'
                }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_post_movies_not_successful(self):
        res = self.client().post('/movies',
            json={
                'title' : 'Movie 1',
                'release_date' : 'invalid date'
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
                'name' : 'Actor 5',
                'age' : 35,
                'gender' : 'M'
                }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_patch_movies_successful(self):
        res = self.client().patch('/movies/3',
            json={
                'title' : 'Movie 5',
                'release_date' : '2015-03-01'
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
                'name' : 'Actor 5',
                'age' : "invalid age",
                'gender' : 'M'
                }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch_movies_not_successful(self):
        res = self.client().patch('/movies/3',
            json={
                'title' : 'Movie 5',
                'release_date' : 'invalid date'
                }, headers=self.auth_header_executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#----------------------------------------# 
# (7) successful DELETE endpoint tests
#----------------------------------------#     

    # def test_delete_actor_successful(self):
    #     res = self.client().delete('/actors/5', headers=self.auth_header_executive)
    #     data = json.loads(res.data)
    #     actor = Actor.query.filter(Actor.id == 5).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(actor, None)

    # def test_delete_movie_successful(self):
    #     res = self.client().delete('/movies/5', headers=self.auth_header_executive)
    #     data = json.loads(res.data)
    #     movie = Movie.query.filter(Movie.id == 5).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(movie, None)

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
                'name' : 'Actor 1',
                'age' : 30,
                'gender' : 'F'
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
                'name' : 'Actor 1',
                'age' : 30,
                'gender' : 'F'
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
                'title' : 'Movie 1',
                'release_date' : '2020-03-01'
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
