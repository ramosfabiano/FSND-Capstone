import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app

#
# Test Class
#
class AppTests(unittest.TestCase):

    # Code that runs once before all test methods
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

    def test_get_actors_all_roles(self):
        for role in self.auth_headers.keys():
            res = self.client().get('/api/v1/actors', headers=self.auth_headers[role])
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(type(data['actors']), type([]))
            self.assertEqual(len(data['actors']), 13)

       
#
# Main
#
if __name__ == "__main__":
    unittest.main()