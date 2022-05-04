import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")


class TestHomePage(unittest.TestCase):
    """Test the app functionality with selenium"""

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


    def test_create_account_title(self):
        """Test that the title of the create a profile page is 'Create
            an Account'"""
        
        # Get the create profile page within the app 
        self.browser.get("http://localhost:5000/create_profile")

        # Check that the title of the create profile page is "Create an Account"
        self.assertEqual(self.browser.title, "Create an Account")


    # def test_log_in_success(self):
    #     """Test that when a user clicks 'log in'
    #         that they are shown to their user profile"""

    #     # Get the homepage where a user will log in
    #     self.browser.get("http://localhost:5000/")

    #     # Get the email information
    #     user_email = self.browser.find_element(By.ID, "email-log-in")
    #     user_email.send_keys("jane@example.com")

    #     # Get the password information
    #     user_password = self.browser.find_element(By.ID, "password-log-in")
    #     user_password.send_keys("password")

    #     # Get the button by its ID and ensure that it is clicked on the browser
    #     button = self.browser.find_element(By.ID, "log-in-button")
    #     button.click()

    #     # Get the result (ensure that we are loading the user profile page)
    #     result = self.browser.get("http://localhost:5000/user_profile")

    #     # Check that the title of the page rendered is "Profile"
    #     self.assertEqual(result.title, "Profile")


    # def test_like_increase(self):
    #     """Test that when a user likes a button, the like count increases"""

    #     # Get the image details page
    #     self.browser.get("http://localhost:5000/user_profile/1")

    #     # Get the like count and set it to a random value
    #     like_count = self.browser.find_element(By.ID, "like-count")
    #     like_count.send_keys("4")

    #     # Get the like button and click it
    #     button = self.browser.find_element(By.ID, "like-button")
    #     button.click()

    #     # Get the updated like count
    #     new_like_count = self.browser.find_element(By.ID, "like-count")

    #     # Assert that the like count increased
    #     assert new_like_count.text == "5"

if __name__ == "__main__":
    unittest.main()