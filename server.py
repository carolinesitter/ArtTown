"""Server for artist by zipcode app"""

from flask import (Flask, render_template, request, flash, session,
                redirect, url_for, jsonify, g)
from model import connect_to_db, db
from datetime import datetime
from random import choice
import crud
import cloudinary.uploader
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dgvuwdtnb"


@app.route("/")
def homepage():
    """View homepage"""
    
    # This is the homepage
    return render_template('homepage.html')


@app.route("/register_profile", methods=["POST"])
def register_profile():
    """Check if account has already been created,
        if not, create new account and add user to db"""

    # Get the information when a user registers an account
    email = request.form.get("email")
    password = request.form.get("password")
    verify_password = request.form.get("verify_password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    instagram = request.form.get("instagram")
    twitter = request.form.get("twitter")
    tiktok = request.form.get("tik_tok")
    website = request.form.get("website")
    zipcode = request.form.get("zipcode")

    # Use crud function to query the database for the user
    user = crud.get_user_by_email(email)
    
    #Check if the user already exists, if not, create a new account
    if user:
        flash("User already registered. Please log in.")
        return redirect("/")
    
    # Ensure that the password and verification are the same 
    elif password != verify_password:
        flash("Sorry! Your passwords do not match. Please try again.")
        redirect("/register_profile")

    else:
        user = crud.create_user(first_name, last_name, username, email,
                password, instagram, twitter, tiktok, website, zipcode)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! Your account has been created. You may now log in!")

    # Send the user back to the homepage
    return redirect("/")        


@app.route("/log_in", methods=["POST"])
def user_login():
    """Log a user in"""

    # Get the email and password from the log in form 
    email = request.form.get("email")
    password = request.form.get("password")

    # Get our user by querying for their email
    user = crud.get_user_by_email(email)

    # If the email/password != the values saved in the database,
    # tell the user to try again. Otherwise, log them in
    if not user or user.password != password:
        flash("Invalid email or password. Please try again.")
        print("invalid password")
        return redirect("/")
    else:
        session['user_email'] = user.email
        session['username'] = user.username

        flash("Successfully logged in!")
        return redirect("/user_profile")


@app.route("/log_out")
def user_logout():
    """Log a user out"""

    # When the user logs out, forget their info in sessions
    session['user_email'] = None
    session['username'] = None

    # Show user back to the homepage
    return redirect("/")


@app.route("/create_profile")
def create_profile():
    """Create a new profile"""

    # Show a new user the form to create an account
    return render_template('create-profile.html')


@app.route("/user_profile")
def user_profile():
    """Show the user's profile"""

    # If a user is logged in, show their profile
    if session["user_email"]:

        # Get the user's email from the session
        email = session['user_email']

        # Use this email to define our user variable
        user = crud.get_user_by_email(email)

        # Get the user's information by querying the user object 
        username = user.username
        zipcode = user.zipcode
        instagram = user.instagram
        tiktok = user.tiktok
        twitter = user.twitter
        website = user.website
        art_collection = user.artist_collection

        # Show the user their profile 
        return render_template('user-profile.html',
                                user=user,
                                username=username,
                                zipcode=zipcode,
                                instagram=instagram,
                                tiktok=tiktok,
                                twitter=twitter,
                                website=website,
                                art_collections=art_collection)

    # If they are not logged in, send the user to the login page
    else:
        return redirect("/")


@app.route("/user_profile/<image_id>", methods=["GET"])
def show_image_info(image_id):
    """Show info about an image"""

    # Get the image information
    image = crud.get_image_by_id(image_id)

    # Get the likes and comments for a particular image
    like_count = len(crud.get_likes_by_image_id(image_id))
    comments = crud.get_comment_by_image_id(image_id = image.image_id)

    # Check that the user is logged in, if so, show them the image details
    if session["user_email"] and image:

        user = crud.get_user_by_email(session.get("user_email"))

        return render_template('image_details.html',
                                user=user, 
                                image=image, 
                                like_count=like_count,
                                comments=comments
                                )


@app.route("/api/user_profile/<image_id>/comments", methods=["POST"])
def add_new_comment(image_id):
    """Allow users to add a comment"""

    # Get the image and comment information from the database
    comment = request.json.get("new_comment")
    image = crud.get_image_by_id(image_id)

    # Add a new comment to the image (and the database)
    if comment and image and session["user_email"]:
        
        user = crud.get_user_by_email(session.get("user_email"))
        user_id = user.user_id
        image_id = image.image_id
        username = user.username

        new_comment = crud.create_comment(comment, image_id, user_id)
        image.comments.append(new_comment)

        db.session.add(image) 
        db.session.commit()

        return jsonify({"status": "OK", "username": username,"comment": comment, "comment_id" : new_comment.comment_id})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/api/user_profile/<image_id>/likes")
def like_an_image(image_id):
    """Allows users to like an image"""

    # Get the image information from the database
    image = crud.get_image_by_id(image_id)

    # Like an image and add that like to the database
    if image and session["user_email"]:
        
        user = crud.get_user_by_email(session.get("user_email"))
        user_id = user.user_id

        like = crud.create_like(image_id, user_id)

        db.session.add(like) 
        db.session.commit()

        return jsonify({"status": "OK", "like_count": len(crud.get_likes_by_image_id(image_id))})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/api/user_profile/<image_id>/remove_likes")
def unlike_an_image(image_id):
    """Allows users to unlike an image"""

    # Get the image information from the database
    image = crud.get_image_by_id(image_id)


    # Remove the like from the image and the database
    if image and session["user_email"]:
        
        user = crud.get_user_by_email(session.get("user_email"))
        user_id = user.user_id

        delete_like = crud.delete_like_by_image_and_user_id(image_id, user_id)

        db.session.delete(delete_like)
        db.session.commit()

        # Return a jsonified like count info to user-interactions.js
        return jsonify({"status": "OK", "like_count": len(crud.get_likes_by_image_id(image_id))})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/api/user_profile/<image_id>/delete_comment", methods=["POST"])
def delete_comment(image_id):
    """Allow users to delete their own comments"""

    # Get the image by id from database
    image = crud.get_image_by_id(image_id)

    # Delete the comment from the database
    if image and session["user_email"]:

        # Query for the comment in the database
        comment = crud.get_comment_by_id(request.json.get("comment_id"))

        # Delete the comment from the database
        db.session.delete(comment)
        db.session.commit()

        # Return jsonified comment info to user-interactions.js
        return jsonify({"status": "OK"})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/api/user_profile/<image_id>/edit_comments", methods=["POST"])
def edit_comment(image_id):
    """Allow users to add a comment"""

    # Get the comment information
    comment_id = request.json.get("comment_id")
    comment_text = request.json.get("comment_text")
    comment = crud.get_comment_by_id(comment_id)

    # Override the previous comment in the database with the new comment
    if comment and session["user_email"]:

        comment.comment = comment_text

        db.session.commit()

        return jsonify({"status": "OK", "comment": comment_text})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/zipcode_input")
def zipcode_input():
    """Show input box where artists can type in zip code"""

    if session["user_email"]:
        
        return render_template('search-by-zip.html')

    else:
        
        return redirect('/')


@app.route("/search_by_zipcode", methods=["POST"])
def search_by_zipcode():
    """Enter in zipcode, show a user profile with matching zip code"""

    # Get the zip code searched on the browser
    zipcode = int(request.form.get("zipcode"))

    # Get the zip code associated with each user's account
    users_with_zip = crud.get_user_by_zipcode(zipcode)

    # From the users with a matching zipcode, choose one at random
    user_zip = choice(users_with_zip)

    # Show the user profile with a matching zip code 
    if user_zip:
        username = user_zip.username
        instagram = user_zip.instagram
        twitter = user_zip.twitter
        tiktok = user_zip.tiktok
        website = user_zip.website
        art_collection = user_zip.artist_collection


        return render_template('user-profile.html',
                                user=user_zip,
                                zipcode=zipcode,
                                user_zip=user_zip,
                                username=username,
                                instagram=instagram,
                                twitter=twitter,
                                tiktok=tiktok,
                                website=website,
                                art_collections=art_collection)
    else:
        flash("Sorry! No results match the Zip Code you entered. Please try again!")
        return redirect('/zipcode_input')


@app.route("/show_random_profile")
def show_random_profile():
    """Show a random artist profile page"""

    # Get the user that is currently logged in
    user_logged_in = session.get("user_email")

    # Query for a random user from our database and assign them to a variable
    random_user = choice(crud.get_all_users())

    # Get the email for our random user object
    random_users_email = random_user.email

    # Make sure that the random user is not the same as the user logged in
    if user_logged_in != random_users_email:
        username = random_user.username
        zipcode = random_user.zipcode
        instagram = random_user.instagram
        twitter = random_user.twitter
        tiktok = random_user.tiktok
        website = random_user.website
        art_collection = random_user.artist_collection


        return render_template('user-profile.html',
                                user = random_user,
                                zipcode=zipcode,
                                username=username,
                                instagram=instagram,
                                twitter=twitter,
                                tiktok=tiktok,
                                website=website,
                                art_collections=art_collection)
        
    else:
        flash("Sorry! We can't find anyone random right now. Try again later.")
        return redirect("/zipcode_input")


@app.route('/explore')
def explore_page():
    """Show all the latest uploads"""

    # Get all the images in the database
    images = crud.get_all_images()

    # Show the explore page
    if session["user_email"]:
    
        return render_template('explore-page.html',
                                images=images,
                                )
    
    else:
        flash("Sorry! You must log in or create an account to view this feature!")
        return redirect('/')


@app.route("/load_art_show")
def load_art_show():
    """Show a random piece of art posted on the platform"""

    # Get the user that is currently logged in
    user_logged_in = session.get("user_email")

    # Query for other users in the database
    users = crud.get_all_not_logged_in_users(user_logged_in)

    # Get a list of our empty users
    random_users = []

    # Loop through our users and make sure they have an art collection
    # Filter out the empty lists 
    for user in users: 
        if user.artist_collection != []:
            random_users.append(user)
    
    # Get a random user
    random_user = choice(random_users)

    # Get the email for our random user object
    random_users_email = random_user.email
    

    # Make sure that the random user is not the same as the user logged in
    if user_logged_in != random_users_email and session["user_email"] and random_users_email:
        username = random_user.username
        first_name = random_user.first_name
        last_name = random_user.last_name
        art_collection = choice(random_user.artist_collection)

        return render_template('art-display.html',
                                random_user=random_user,
                                username=username,
                                first_name=first_name,
                                last_name=last_name,
                                art_collection=art_collection)
    
    else:
        flash("Sorry! You need to be logged in to access the art show!")
        return redirect("/")


@app.route('/art_show_user_profile/<user_id>')
def show_art_show_profile(user_id):
    """Show the profile of the user from the art show"""

    # Get the user from the art show
    art_show_user = crud.get_user_by_id(user_id)

    # Get the random user's information by querying the user object 
    username = art_show_user.username
    zipcode = art_show_user.zipcode
    instagram = art_show_user.instagram
    tiktok = art_show_user.tiktok
    twitter = art_show_user.twitter
    website = art_show_user.website
    art_collection = art_show_user.artist_collection

    # Show the user their profile 
    return render_template('user-profile.html',
                            user=art_show_user,
                            username=username,
                            zipcode=zipcode,
                            instagram=instagram,
                            tiktok=tiktok,
                            twitter=twitter,
                            website=website,
                            art_collections=art_collection)


@app.route("/create_post_form")
def create_new_post():
    """Render template for artists to upload images to their profile"""

    # Show the page to create a new post
    return render_template('create-post.html')


@app.route("/create_art_collection", methods=["POST"])
def create_art_collection():
    """Get art collection and user data from browser and add to db"""

    # Get the user information
    email = session['user_email']
    user = crud.get_user_by_email(email)

    # Get the digital art gallery information
    gallery_title = request.form.get("gallery-title")
    gallery_description = request.form.get("gallery-description")

    # Create the new art gallery post
    if gallery_title and gallery_description:

        artist_gallery = crud.create_artist_collection(gallery_title, gallery_description, user)
        db.session.add(artist_gallery)
        db.session.commit()

        flash("Congratulations! You have created your gallery. Now you can add photos!")
        return render_template('upload-image.html', artist_gallery=artist_gallery)

    else:
        flash("Sorry, you must give your gallery a name and description. Please try again.")
        return render_template('create-post.html')


@app.route("/upload_image", methods=["POST"])
def process_upload_data():
    """Process form data and return the url generated by Cloudinary"""

    # Get the user and art post information
    email = session['user_email']
    user = crud.get_user_by_email(email)
    user_id = user.user_id
    artist_collection = crud.get_art_collection_by_id(int(request.form.get('gallery-collection')))
    image_title = request.form.get('image-title')
    date_uploaded = datetime.now()
    
    # Get the filename from the uploaded image
    filename = request.files['filename']

    # Get the result and image link from the Cloudinary API
    result = cloudinary.uploader.upload(filename,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME)
    image_link = result['secure_url']

    # Create the new image and add it to the user profile (and database)
    if image_link and image_title:

        new_image = crud.create_image(image_title, image_link, date_uploaded, artist_collection, user_id)
        db.session.add(new_image)
        db.session.commit()

        return redirect("/user_profile")
    else:
        return render_template('upload-image.html')

    
@app.route("/add_images_to_collection")
def add_images_to_to_collection():
    """Allow users to add an image to an already existing artist collection"""

    # Get the user and art collection information 
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    user_id = user.user_id
    art_collections = crud.get_all_art_collections_by_user(user_id)

    return render_template('add-images.html',
                            user=user,
                            user_id=user_id,
                            art_collections=art_collections)


@app.route("/user_profile/edit/<artist_collection_id>")
def show_art_collection_details(artist_collection_id):
    """Show the user details about their artist collection"""

    # Get the artist collection by its ID
    art_collection = crud.get_art_collection_by_id(artist_collection_id)

    # Get the image(s) by Artist Collection ID
    images = crud.get_images_in_art_collection(artist_collection_id)

    #Ensure to check that the user is logged in
    if session["user_email"]:

        user = crud.get_user_by_email(session.get("user_email"))

        # Show the user their post details so that they can edit
        return render_template('art-collection-details.html',
                                art_collection=art_collection,
                                images=images,
                                user=user)


@app.route("/user_profile/edit/<artist_collection_id>/post_title", methods=["POST"])
def edit_post_title(artist_collection_id):
    """Allow the user to edit their post title"""

    # Get the artist collection by its ID
    art_collection = crud.get_art_collection_by_id(artist_collection_id)

    # Get the edited/ new title from the browser
    gallery_title_text = request.json.get("gallery_title_text")

    # Get the old gallery title
    gallery_title = art_collection.gallery_title

    # Override the previous gallery title in the db with the new title
    if gallery_title and session["user_email"]:

        gallery_title = gallery_title_text

        db.session.commit()

        return jsonify({"status": "OK", "gallery_title": gallery_title_text})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/user_profile/edit/<artist_collection_id>/desc", methods=["POST"])
def edit_description(artist_collection_id):
    """Allow the user to edit their post description"""

    # Get the artist collection by its ID
    art_collection = crud.get_art_collection_by_id(artist_collection_id)

    # Get the edited gallery description from the browser
    gallery_description_text = request.json.get("gallery_description_text")

    # Get the old gallery description
    gallery_description = art_collection.gallery_description

    # Override the previous gallery title in the db with the new description
    if gallery_description and session["user_email"]:

        gallery_description = gallery_description_text

        db.session.commit()

        return jsonify({"status": "OK", "gallery_description": gallery_description_text})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/user_profile/edit/<artist_collection_id>/img_title", methods=["POST"])
def edit_image_title(artist_collection_id):
    """Allow a user to edit their image title"""

    # Get the artist collection by its ID
    art_collection = crud.get_art_collection_by_id(artist_collection_id)

    image_id = request.json.get("image_id")

    # Get the image
    image = crud.get_image_by_id(image_id)

    # Get the edited image title from the browser
    image_title_text = request.json.get("image_title_text")

    # Override the previous image title in the db with the new image title
    if image.image_title and session["user_email"]:

        image.image_title = image_title_text

        db.session.commit()

        return jsonify({"status": "OK", "image_title": image_title_text})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/user_profile/edit/<artist_collection_id>/delete_img", methods=["POST"])
def delete_image_from_collection(artist_collection_id):
    """Allow the user to delete images from their artist collection"""

    # Get the artist collection by its ID
    art_collection = crud.get_art_collection_by_id(artist_collection_id)

    if art_collection and session["user_email"]:

        # Get the image object
        image = crud.get_image_by_id(request.json.get("image_id"))

        # Delete the image from the database
        db.session.delete(image)
        db.session.commit()

        return jsonify({"status": "OK"})
    
    else:
        return jsonify({"status": "FAILED"})


@app.route("/user_profile/edit/<artist_collection_id>/del_post", methods=["POST"])
def delete_artist_collection(artist_collection_id):
    """Allow a user to delete their entire artist collection/post"""

    #Get the artist collection ID
    artist_collection_id = request.json.get("artist_collection_id")

    art_collection = crud.get_art_collection_by_id(artist_collection_id)

    # Get all of the images within that artist collection
    images_in_collection = crud.get_images_in_art_collection(artist_collection_id)


    if art_collection and session["user_email"]:

        for image in images_in_collection:
            db.session.delete(image)

        db.session.delete(art_collection)

        db.session.commit()

        return jsonify({"status": "OK"})

    else:
        return jsonify({"status": "FAILED"})



if __name__ == "__main__":

    import sys
    # Code to run the selenium tests in the terminal 
    if sys.argv[-1] == "selenium_test":
        connect_to_db(app, "postgresql:///testdb")

    # Otherwise, run the server normally 
    else:
        connect_to_db(app)

    app.run(host="0.0.0.0", debug=True)