"""Basic query operations."""

from model import db, User, ArtistCollection, Image, Comment, Like, connect_to_db


# Create a new user
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

# Create a new artist collection
def create_artist_collection(gallery_title, gallery_description, user):
    """Create and return a new art collection"""

    art_collection = ArtistCollection(
                    gallery_title=gallery_title,
                    gallery_description=gallery_description,
                    #user object
                    user=user
                    )
    
    return art_collection

# Create a new image
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

# Create a new comment
def create_comment(comment, image_id, user_id):

    new_comment = Comment(
                    comment=comment,
                    image_id=image_id,
                    user_id=user_id,
                    )

    return new_comment

# Create a new like
def create_like(image_id, user_id):

    new_like = Like(
                    image_id=image_id,
                    user_id=user_id,
                    )

    return new_like

# Get the total of likes for an image
def get_likes_by_image_id(image_id):
    """Return all likes by image id"""

    return Like.query.filter(Like.image_id == image_id).all()

# Get the artist collection by its id
def get_art_collection_by_id(artist_collection_id):
    """Return artist collection by id"""

    return ArtistCollection.query.get(artist_collection_id)

# Get the image by its id
def get_image_by_id(image_id):
    """Return an image by id"""

    return Image.query.get(image_id)

# Get the user by their id
def get_user_by_id(user_id):
    """Return a user by id"""

    return User.query.get(user_id)

# Get the comment by their id
def get_comment_by_id(comment_id):
    """Return a comment by id"""

    return Comment.query.get(comment_id)

# Get the comments for a particular image
def get_comment_by_image_id(image_id):
    """Return a comment by image id"""

    return Comment.query.filter(Comment.image_id == image_id).all()

# Get a like made by a particular user for a particular image
def delete_like_by_image_and_user_id(image_id, user_id):
    """Return likes that have been made with a particular image and user id"""

    return Like.query.filter((Like.image_id == image_id) & (Like.user_id == user_id)).first()

# Get a comment made by a particular user for a particular image
def get_comment_by_image_and_user_id(image_id, user_id):
    """Return comments made with a particular image and user id"""

    return Comment.query.filter((Comment.image_id == image_id) & (Comment.user_id == user_id)).first()

# Get a users artist collections
def get_user_art_collections(artist_collection_id):
    """Return a user by artist collection id"""

    return User.query.filter(User.artist_collection == artist_collection).first()

# Get a users images in their art collection
def get_art_collection_images(image_id):
    """Return an art collection by image id"""

    return ArtCollection.query.filter(ArtCollection.image_id == image_id).all()

# Get a user by their email
def get_user_by_email(email):
    """Return a user by their email"""

    return User.query.filter(User.email == email).first()

# Get a user by their zipcode
def get_user_by_zipcode(zipcode):
    """Return a user by zipcode"""

    return User.query.filter(User.zipcode == zipcode).first()

# Get all of our users
def get_all_users():
    """Get all users in our users table"""

    return User.query.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)