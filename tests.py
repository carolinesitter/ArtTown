import os
import unittest

from datetime import datetime

from server import app
from model import db, connect_to_db, User, ArtistCollection, Image, Like, Comment, example_data

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

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
                                    data={"email":"jane@wrongemail.com",
                                            "password":"password"},
                                    follow_redirects = True)

        # Check that the user is redirected to the homepage
        self.assertIn(b"Log In", result.data)


    def test_sign_in_fail_wrong_password(self):
        """Test for a sign in error if a user enters the wrong password"""

        # Attempt to log in test user with the wrong password
        result = self.client.post("/log_in",
                                    data={"email":"jane@example.com",
                                            "password":"wrongpassword"},
                                    follow_redirects = True)

        # Check that the user is redirected to the homepage
        self.assertIn(b"Log In", result.data)
    

    def test_log_in_success(self):
        """Test that a user can log in sucessfully"""

        # Log in our test user with the correct information
        result = self.client.post("/log_in",
                                    data={"email":"jane@example.com",
                                            "password":"password"},
                                    follow_redirects = True)

        # Check that the user is redirected to their profile page
        self.assertIn(b"Profile", result.data)


    def test_search_by_zipcode(self):
        """Test that a user can access the search by zipcode form"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)
        
        # Test that the zipcode information will search for a user by their zipcode
        result = self.client.post("/search_by_zipcode",
                                    data={"zipcode": "00000"},
                                    follow_redirects = True)

        # Check that the user is redirected to a profile page
        # with the matching zipcode input
        self.assertIn(b"Profile", result.data)


    def test_show_image_details_page(self):
        """Test that a user can view the image details on a user profile"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)

        # Test that the image details will be properly rendered
        result = self.client.get("/user_profile/1")

        # Check that the user is shown the image details page
        self.assertIn(b"Image Details", result.data)


    def test_show_like_button(self):
        """Test that a user is shown a like button on the image details page"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)

        # Test that we are shown the image details page
        result = self.client.get("/user_profile/1")

        # Check that the user is shown the like button
        self.assertIn(b"Like", result.data)

    
    def test_like_count_increase(self):
        """Test that the user can like an image"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)
        
        # Test that we are getting the like count data
        result = self.client.get("/api/user_profile/1/likes")

        # Test that the like count increases
        self.assertIn(b"2", result.data)

    def test_like_count_decrease(self):
        """Test that the user can unlike an image"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)
        
        # Test that we are getting the like count data
        result = self.client.get("/api/user_profile/1/remove_likes")

        # Test that the like count decreases
        self.assertIn(b"0", result.data)

    def test_add_comment(self):
        """Test that a user can leave a comment on an image"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)
        
        # Check that the comment is added to the database
        result = self.client.post("/api/user_profile/1/comments",
                                    json={"new_comment": "Nice work"})

        # Check that the comment is showing up on the web page
        self.assertIn(b"Nice work", result.data)

    
    def test_delete_comment(self):
        """Test that a user can delete their comment on an image"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)

        # Check that the comment exists in the database and delete it
        result = self.client.post("/api/user_profile/1/delete_comment", 
                                    json={"comment_id":1})

        # Check that the comment is deleted from the web page
        self.assertNotIn(1, result.data)

    
    def test_edit_comment(self):
        """Test that a user can edit their comment"""

        # Log in our test user
        self.client.post("/log_in",
                        data={"email":"jane@example.com",
                                "password":"password"},
                        follow_redirects = True)
        
        # Check that the comment exists in the database and edit it
        result = self.client.post("/api/user_profile/1/edit_comments", 
                                    json={"comment_text": "Nice job",
                                            "comment_id":1})
        
        # Check that the edited comment is what displays on the web page
        self.assertIn(b"Nice job", result.data)

class TestHomePage(unittest.TestCase):

    def setUp(self):
        """Stuff to set up our tests"""

        # Set up our webdriver
        self.browser = webdriver.Chrome("chromedriver", options=chrome_options)

    def tearDown(self):
        """Stuff to tear down our tests"""

        # Close our webdriver after each test
        self.browser.quit()

    def test_homepage_title(self):
        """Test that the title of the homepage is 'Welcome''"""

        # Get the homepage of the app 
        self.browser.get("http://localhost:5000/")

        # Check that the title of the homepage is "Welcome"
        self.assertEqual(self.browser.title, "Welcome")

if __name__ == "__main__":
    unittest.main()