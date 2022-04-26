"""CRUD operations."""

from model import db, User, ArtistCollection, Image, Comment, Like, connect_to_db


# insert functions and query statements in order to:
# - parse through our data
# - create query statements 


def create_user(first_name, last_name, username, email,
                password, instagram, twitter, tiktok, website, zipcode):
    """Create and return a new user."""

    user = User(first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                instagram=instagram,
                twitter=twitter,
                tiktok=tiktok,
                website=website,
                zipcode=zipcode
                )

    return user


def create_artist_collection(gallery_title, gallery_description, user):
    """Create and return a new art collection"""

    art_collection = ArtistCollection(
                    gallery_title=gallery_title,
                    gallery_description=gallery_description,
                    #user object
                    user=user
                    )
    
    return art_collection


def create_image(image_title, image_link, date_uploaded, artist_collection):
    """Create and return a new image"""

    new_image = Image(
                image_title=image_title,
                image_link=image_link,
                date_uploaded=date_uploaded,
                # artist collection object
                artist_collection=artist_collection
                )

    return new_image


def create_comment(comment, image_id, user_id):

    new_comment = Comment(
                    comment=comment,
                    image_id=image_id,
                    user_id=user_id,
                    )

    return new_comment


def create_like(like, image_id, user_id):

    new_like = Like(
                    like=like,
                    image_id=image_id,
                    user_id=user_id,
                    )

    return new_like

def get_art_collection_by_id(artist_collection_id):
    """Return artist collection by id"""

    return ArtistCollection.query.get(artist_collection_id)


def get_image_by_id(image_id):
    """Return an image by id"""

    return Image.query.get(image_id)


def get_user_by_id(user_id):
    """Return a user by id"""

    return User.query.get(user_id)


def get_user_art_collections(artist_collection_id):
    """Return a user by artist collection id"""

    return User.query.filter(User.artist_collection == artist_collection).first()


def get_art_collection_images(image_id):
    """Return an art collection by image id"""

    return ArtCollection.query.filter(ArtCollection.image_id == image_id).all()


def get_user_by_first_name(first_name):
    """Return a user by first name"""

    return User.query.filter(User.first_name == first_name).first()


def get_user_by_last_name(last_name):
    """Return a user by last_name"""

    return User.query.filter(User.last_name == last_name).first()


def get_user_by_email(email):
    """Return a user by their email"""

    return User.query.filter(User.email == email).first()


def get_user_by_password(password):
    """Return a user by their password"""

    return User.query.filter(User.password == password).first()


def get_user_by_zipcode(zipcode):
    """Return a user by zipcode"""

    return User.query.filter(User.zipcode == zipcode).first()


def get_user_by_username(username):
    """Return a user by username"""

    return User.query.filter(User.username == username).first()


def get_user_by_instagram(instagram):
    """Return a user by instagram"""

    return User.query.filter(User.instagram == instagram).first()


def get_user_by_twitter(twitter):
    """return a user by twitter"""

    return User.query.filter(User.twitter == twitter).first()


def get_user_by_titkok(tiktok):
    """Return a user by tiktok"""

    return User.query.filter(User.tiktok == tiktok).first()


def get_user_by_twitter(twitter):
    """Return a user by twitter"""

    return User.query.filter(User.twitter == twitter).first()


def get_user_by_website(website):
    """Return a user by website"""

    return User.query.filter(User.website == website).first()




if __name__ == '__main__':
    from server import app
    connect_to_db(app)