import unittest, sys, os

sys.path.append('../PlantParenthood) # imports python file from parent directory
from app import app, db

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    ###############
    #### tests ####
    ###############

    def signup(self, username, email, password):
        return self.app.post('/signup',
                            data=dict(username=username,
                                      email=email,
                                      password=password, 
                                      confirm_password=password),
                            follow_redirects=True)

    def test_valid_user_registration(self):
        response = self.signup('test', 'test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def test_invalid_username_registration(self):
        response = self.signup('t', 'test@example.com', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)
        response = self.signup('trestristestrigrestragantrigoenuntrigal', 'test@example.com', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)

    def test_invalid_email_registration(self):
        response = self.signup('test2', 'test@example', 'FlaskIsAwesome')
        self.assertIn(b'Invalid email address.', response.data)
        response = self.signup('test2', 'testexample.com', 'FlaskIsAwesome')
        self.assertIn(b'Invalid email address.', response.data)

    def login(self, username, password):
        return self.app.post('/login',
                            data=dict(username=username,
                                      password=password),
                            follow_redirects=True)
    
    def test_valid_user_login(self):
        response = self.login('test', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()