import unittest, sys

sys.path.append('../PlantParenthood') # imports python file from parent directory
from app import app

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def signup(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def home_page(self):
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def portfolio(self):
        response = self.app.post('/portfolio,', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def add_to_portfolio(self):
        response = self.app.post('/add_to_portfolio,', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def rename_plant(self):
        response = self.app.post('/rename_plant,', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()