import unittest

from datetime import datetime

from server import app
from model import db, connect_to_db, User, ArtistCollection, Image, Like, Comment, example_data

class CreateProfileTests(unittest.TestCase):
    """Flask tests that use the database""" 

    def setUp(self):
        """Set up the testing requirements"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect to our test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables with sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Drop the database at the end of every test"""
    
        # Drop the database at the end of every test
        db.session.close()
        db.drop_all()

    def test_create_profile_registers_new_user(self):
        """ Test that creating a profile will register a new user"""

        # Add a new test user to the database
        result = self.client.post("/register_profile", 
                                    data={"first_name":"Bob",
                                        "last_name":"Ross",
                                        "email":"bob@example.com",
                                        "username":"bobross",
                                        "password":"password",
                                        "verify_password":"password",
                                        "zipcode": "00000",
                                        "instagram": None,
                                        "twitter": None,
                                        "tik_tok": None,
                                        "website": None}, 
                                    follow_redirects = True)
        
        # Checking if the bite string is in the html and result data
        # Check for a string not dependent on a flash message
        self.assertIn(b"Log In", result.data)

        # # Define a test user by querying the database for the first name
        test_user = User.query.filter(User.first_name == "Bob").first()

        # Verify that the user's email is bob@example.com
        self.assertTrue(test_user.email == "bob@example.com")

        # Verify that the user's username is bobross
        self.assertTrue(test_user.username == "bobross")


    def test_register_fail_user_already_exists(self):
        """Test for a sign up error if a user already exists"""

        # Attempt to register an account as an already existing user
        result = self.client.post("/register_profile", 
                                    data={"first_name":"Jane",
                                        "last_name":"Doe",
                                        "email":"doe@example.com",
                                        "username":"janedoe",
                                        "password":"password",
                                        "instagram":"@janedoe",
                                        "twitter":"@janetwitter",
                                        "tiktok":"@janetok",
                                        "website":"www.janedoe.com",
                                        "zipcode":"00000"}, 
                                    follow_redirects = True)

        # Assert that the user is redirected to the homepage
        self.assertIn(b"Log In", result.data)

    def test_sign_in_fail_wrong_email(self):
        """Test for a sign in error if a user enters the wrong email"""

        # Attempt to log in test user with the wrong email
        result = self.client.post("/log_in",
                                    data={"email": "jane@wrongemail.com",
                                            "password": "password"},
                                    follow_redirects = True)

        # Check that the user is redirected to the homepage
        self.assertIn(b"Log In", result.data)


    def test_sign_in_fail_wrong_password(self):
        """Test for a sign in error if a user enters the wrong password"""

        # Attempt to log in test user with the wrong password
        result = self.client.post("/log_in",
                                    data={"email": "jane@example.com",
                                            "password": "wrongpassword"},
                                    follow_redirects = True)

        # Check that the user is redirected to the homepage
        self.assertIn(b"Log In", result.data)
    




if __name__ == "__main__":
    unittest.main()