"""CRUD operations."""

from model import db, User, ArtistCollection, Image, connect_to_db


# insert functions and query statements in order to:
# - parse through our data
# - create query statements 


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def add_artist_collection(user, title, description):
    """Create and return a new art collection"""

    art_collection = ArtCollection(
                    user=user,
                    title=title,
                    description=description,
                    )
    
    return art_collection


def add_image(art_collection, title, link):
    """Create and return a new image"""

    new_image = Image(
                art_collection=art_collection,
                title=title,
                link=link
                )

    return image

def get_art_collection_by_id(artist_collection_id):
    """Return artist collection by id"""

    return ArtistCollection.query.get(artist_collection_id)


def get_image_by_id(image_id):
    """Return an image by id"""

    return Image.query.get(image_id)


def get_user_by_id(user_id):
    """Return a user by id"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by their email"""

    return User.query.filter(User.email == email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)