import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from model import Actor, Movie, ActorMovieAssociation
from schemas.actor import *
from schemas.movie import *
from schemas.actor_movie import *

#
# Test Class
#
class AppTests(unittest.TestCase):

    # runs once before all test methods
    @classmethod
    def setUpClass(self):
        self.app = create_app()
        self.client = self.app.test_client

        with open('tests/auth.json', 'r') as f:
            self.auth = json.loads(f.read())
        
        assistant_token = self.auth["roles"]["assistant"]["access_token"]
        director_token = self.auth["roles"]["director"]["access_token"]
        producer_token = self.auth["roles"]["producer"]["access_token"]
        self.auth_headers = {
            'assistant': { 'Authorization': f'Bearer {assistant_token}'},
            'director':  { 'Authorization': f'Bearer {director_token}'},
            'producer':  { 'Authorization': f'Bearer {producer_token}'}
        }
        
    # runs before each test
    def setUp(self):
        pass
        
    # runs after each test
    def tearDown(self):
        pass

    #
    # GET
    #
    def test_get_actors_all_roles(self):
        for role in self.auth_headers.keys():
            res = self.client().get('/api/v1/actors', headers=self.auth_headers[role])
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(type(data['actors']), type([]))

    def test_get_movies_all_roles(self):
        for role in self.auth_headers.keys():
            res = self.client().get('/api/v1/movies', headers=self.auth_headers[role])
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(type(data['movies']), type([]))

    #
    # PATCH
    #
    def test_patch_actor_not_authorized(self):
        role = 'assistant'
        # get random actor
        res = self.client().get('/api/v1/actors', headers=self.auth_headers[role])
        data = json.loads(res.data)
        random_actor = data['actors'][0]
        actor = ActorPatchRepresentation(Actor(name=random_actor['name'], gender=random_actor['gender'], birth_date=random_actor['birth_date'], nationality=random_actor['nationality']))
        # try to patch it
        res = self.client().patch(f'/api/v1/actors/{random_actor["id"]}', data=actor, headers=self.auth_headers[role])
        self.assertEqual(res.status_code, 403)
  
    def test_patch_actor(self):
        for role in ['director', 'producer']:
            # get random actor
            res = self.client().get('/api/v1/actors', headers=self.auth_headers[role])
            data = json.loads(res.data)
            random_actor = data['actors'][0]
            actor = ActorPatchRepresentation(Actor(name=random_actor['name'], gender=random_actor['gender'], birth_date=random_actor['birth_date'], nationality=random_actor['nationality']))
            # patch it
            res = self.client().patch(f'/api/v1/actors/{random_actor["id"]}', data=actor, headers=self.auth_headers[role])
            self.assertEqual(res.status_code, 200)
 
    def test_patch_actor_not_found(self):
        for role in ['director', 'producer']:
            random_id = 999999
            actor = ActorPatchRepresentation(Actor(name='any', gender='any', birth_date='any', nationality='any'))
            res = self.client().patch('/api/v1/actors/random_id', data=actor, headers=self.auth_headers[role])
            self.assertEqual(res.status_code, 404)
 
    def test_patch_actor_fail_invalid_data(self):
        for role in ['director', 'producer']:
            # get random actor
            res = self.client().get('/api/v1/actors', headers=self.auth_headers[role])
            data = json.loads(res.data)
            random_actor = data['actors'][0]
            actor = ActorPatchRepresentation(Actor(name=random_actor['name'], gender=random_actor['gender'], birth_date='INVALID_DATE', nationality=random_actor['nationality']))
            # patch it
            res = self.client().patch(f'/api/v1/actors/{random_actor["id"]}', data=actor, headers=self.auth_headers[role])
            self.assertEqual(res.status_code, 422)

    def test_patch_movie_not_authorized(self):
        role = 'assistant'
        # get random movie
        res = self.client().get('/api/v1/movies', headers=self.auth_headers[role])
        data = json.loads(res.data)
        random_movie = data['movies'][0]
        movie = MoviePatchRepresentation(Movie(title=random_movie['title'], genre=random_movie['genre'], release_date=random_movie['release_date']))
        # try to patch it
        res = self.client().patch(f'/api/v1/movies/{random_movie["id"]}', data=movie, headers=self.auth_headers[role])
        self.assertEqual(res.status_code, 403)
   
    def test_patch_movie(self):
        for role in ['director', 'producer']:
            # get random movie
            res = self.client().get('/api/v1/movies', headers=self.auth_headers[role])
            data = json.loads(res.data)
            random_movie = data['movies'][0]
            movie = MoviePatchRepresentation(Movie(title=random_movie['title'], genre=random_movie['genre'], release_date=random_movie['release_date']))
            # patch it
            res = self.client().patch(f'/api/v1/movies/{random_movie["id"]}', data=movie, headers=self.auth_headers[role])
            self.assertEqual(res.status_code, 200)

    def test_patch_movie_not_found(self):
        for role in ['director', 'producer']:
            random_id = 999999
            movie = MoviePatchRepresentation(Movie(title='any', genre='any', release_date='any'))
            res = self.client().patch('/api/v1/movies/random_id', data=movie, headers=self.auth_headers[role])
            self.assertEqual(res.status_code, 404)
    
    def test_patch_movie_fail_invalid_data(self):
        for role in ['director', 'producer']:
            # get random movie
            res = self.client().get('/api/v1/movies', headers=self.auth_headers[role])
            data = json.loads(res.data)
            random_movie = data['movies'][0]
            movie = MoviePatchRepresentation(Movie(title=random_movie['title'], genre=random_movie['genre'], release_date='INVALID_DATE'))
            # patch it
            res = self.client().patch(f'/api/v1/movies/{random_movie["id"]}', data=movie, headers=self.auth_headers[role])
            self.assertEqual(res.status_code, 422)
               
    #
    # POST
    #
    def test_post_actor_not_authorized(self):
        #fail for assistant
        pass
  
    def test_post_actor(self):
        # for director and producer
        pass
 
    def test_post_actor_fail_invalid_data(self):
        # for director OR producer, invalid data
        pass

    def test_post_movie_not_authorized(self):
        #fail for assistant
        pass
  
    def test_post_movie(self):
        # for director and producer
        pass
 
    def test_post_movie_fail_invalid_data(self):
        # for director OR producer, invalid data
        pass

    def test_post_actor_movie_not_authorized(self):
        pass
    
    def test_post_actor_movie(self):
        # for director and producer
        pass
 
    def test_post_actor_movie_invalid_actor(self):
        # for director OR producer, invalid data
        pass
    
    def test_post_actor_movie_invalid_movie(self):
        # for director OR producer, invalid data
        pass
        
    #
    # DELETE
    #    
    def test_delete_actor_not_authorized(self):
        #fail for assistant
        pass
       
    def test_delete_actor_not_found(self):
         # for director and producer
        pass      

    def test_delete_actor(self):
         # for director and producer
        pass          

    def test_delete_movie_not_authorized(self):
        #fail for assistant
        pass
       
    def test_delete_movie_not_found(self):
         # for director and producer
        pass      

    def test_delete_movie(self):
         # for director and producer
        pass

    def test_delete_actor_movie_not_authorized(self):
        pass
    
    def test_delete_actor_movie(self):
        # for director and producer
        pass
 
    def test_delete_actor_movie_invalid_actor(self):
        # for director OR producer, invalid data
        pass
    
    def test_delete_actor_movie_invalid_movie(self):
        # for director OR producer, invalid data
        pass
           
#
# Main
#
if __name__ == "__main__":
    unittest.main()