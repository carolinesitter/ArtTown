import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")


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