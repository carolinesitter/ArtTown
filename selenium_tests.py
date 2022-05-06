import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from server import app
from model import db, connect_to_db, User, ArtistCollection, Image, Like, Comment, example_data
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")


class TestHomePage(unittest.TestCase):
    """Test the app functionality with selenium"""

    def setUp(self):
        """Stuff to set up our tests"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect to our test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables with sample data
        db.drop_all()
        db.create_all()
        example_data()
        
        # Set up our webdriver
        self.browser = webdriver.Chrome("chromedriver", options=chrome_options)


    def tearDown(self):
        """Stuff to tear down our tests"""

        # Drop the database at the end of every test
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

        # Close our browser after each test
        self.browser.quit()
        

    def test_homepage_title(self):
        """Test that the title of the homepage is 'Welcome''"""

        # Get the homepage of the app 
        self.browser.get("http://localhost:5000/")

        # Check that the title of the homepage is "Welcome"
        self.assertEqual(self.browser.title, "Welcome")


    def test_create_account_title(self):
        """Test that the title of the create a profile page is 'Create
            an Account'"""
        
        # Get the create profile page within the app 
        self.browser.get("http://localhost:5000/create_profile")

        # Check that the title of the create profile page is "Create an Account"
        self.assertEqual(self.browser.title, "Create an Account")


    def test_log_in_success(self):
        """Test that when a user clicks 'log in'
            that they are shown to their user profile""" 

        # Get the homepage where a user will log in
        self.browser.get("http://localhost:5000/")

        # Get the email and password information
        user_email = self.browser.find_element(By.ID, "email-log-in")
        user_password = self.browser.find_element(By.ID, "password-log-in")


        # Pass in the log in info
        user_email.send_keys("jane@example.com")
        user_password.send_keys("password")


        # Get the button by its ID and ensure that it is clicked on the browser
        form = self.browser.find_element(By.ID, "log-in-form")
        form.submit()
    

        # Assert that the user profile url has loaded
        actual_url="http://localhost:5000/user_profile"
        expected_url= self.browser.current_url
        self.assertEqual(expected_url, actual_url)


    def test_like_increase(self):
        """Test that when a user likes a button, the like count increases"""

        # Get the log in page
        self.browser.get("http://localhost:5000/")

        # Get the email and password information
        user_email = self.browser.find_element(By.ID, "email-log-in")
        user_password = self.browser.find_element(By.ID, "password-log-in")


        # Pass in the log in info
        user_email.send_keys("jane@example.com")
        user_password.send_keys("password")


        # Get the button by its ID and ensure that it is clicked on the browser
        form = self.browser.find_element(By.ID, "log-in-form")
        form.submit()

        # Get the image details page
        self.browser.get("http://localhost:5000/user_profile/1")

        # Get the like button and click it
        button = self.browser.find_element(By.ID, "like-button")
        button.click()

        # Get the updated like count
        new_like_count = self.browser.find_element(By.ID, "like-count")

        # Assert that the like count increased
        assert new_like_count.text == "1"

if __name__ == "__main__":
    unittest.main()