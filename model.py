"""Models for Artist by Zip Code app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """User model for app"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    instagram = db.Column(db.String(50))
    twitter = db.Column(db.String(50))
    tiktok = db.Column(db.String(50))
    website = db.Column(db.String(50), unique=True)
    zipcode = db.Column(db.Integer, nullable=False)


    artist_collection = db.relationship('ArtistCollection', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    likes = db.relationship('Like', back_populates='user')


    def __repr__(self):
        """Show info about each user object"""

        return f"""<User Id = {self.user_id},
                    First Name = {self.first_name},
                    Last Name = {self.last_name},
                    Email = {self.email},
                    Username = {self.username}>"""


class ArtistCollection(db.Model):
    """Artist collection model for app"""

    __tablename__ = "artist_collections"

    artist_collection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    gallery_title = db.Column(db.String, nullable=False)
    gallery_description = db.Column(db.String, nullable=False)


    user = db.relationship('User', back_populates='artist_collection')
    image = db.relationship('Image', back_populates='artist_collection')


    def __repr__(self):
        """Show info about each artist collection object"""

        return f"""<Artist Collection ID = {self.artist_collection_id},
                    User ID = {self.user_id},
                    Gallery Title = {self.gallery_title},
                    Gallery Description = {self.gallery_description}>"""


class Image(db.Model):
    """Image model for app"""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_collection_id = db.Column(db.Integer, db.ForeignKey("artist_collections.artist_collection_id"))
    image_title = db.Column(db.String(50), nullable=False)
    image_link = db.Column(db.String, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False)


    artist_collection = db.relationship('ArtistCollection', back_populates='image')
    comments = db.relationship('Comment', back_populates='image')
    likes = db.relationship('Like', back_populates='image')


    def __repr__(self):
        """Show info about each image object"""

        return f"""<Image ID = {self.image_id},
                    Artist Collection ID = {self.artist_collection_id},
                    Image Title = {self.image_title},
                    Image Link = {self.image_link},
                    Date Uploaded = {self.date_uploaded}>"""


class Comment(db.Model):
    """Comments model for app"""

    ___tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(250), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.image_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


    image = db.relationship('Image', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

    def __repr__(self):
        """Show info about each comment object"""

        return f"""<Comment ID = {self.comment_id},
                    Comment = {self.comment},
                    Image ID = {self.image_id}>"""
    

class Like(db.Model):
    """Likes model for app"""

    __tablename__ = "likes"

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    like = db.Column(db.Integer) # remove this eventually!! 
    image_id = db.Column(db.Integer, db.ForeignKey("images.image_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    image = db.relationship('Image', back_populates='likes')
    user = db.relationship('User', back_populates='likes')

    def __repr__(self):
        """Show info about each like object"""

        return f"""<Like ID = {self.like_id},
                    Like = {self.like},
                    Image ID = {self.image_id},
                    User ID = {self.user_id}>"""


def connect_to_db(flask_app, db_uri="postgresql:///artists-by-zip", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    #Call connect_to_db(app, echo=False)

    connect_to_db(app)