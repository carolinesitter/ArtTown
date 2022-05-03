import unittest

from datetime import datetime

from server import app
from model import db, connect_to_db, User, ArtistCollection, Image, Like, Comment, example_data

class CreateProfileTests(unittest.TestCase):
    """Flask tests that use the database""" 

    def setUp(self):
        """Set up the testing requirements"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key123'
        self.client = app.test_client()

        # Connect to our test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables with sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Drop the database at the end of every test"""
    
        # Drop the database
        db.session.close()
        db.drop_all()

    def test_create_profile_registers_new_user(self):













if __name__ == "__main__":
    unnittest.main()