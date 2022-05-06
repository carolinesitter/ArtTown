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

JS_TESTING_MODE = False
@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


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

    # When the user logs out, forget their email in sessions
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
                                username=username,
                                zipcode=zipcode,
                                instagram=instagram,
                                tiktok=tiktok,
                                twitter=twitter,
                                website=website,
                                art_collection=art_collection)

    # If they are not logged in, send the user to the login page
    else:
        return redirect("/")


@app.route("/user_profile/<image_id>", methods=["GET"])
def show_image_info(image_id):
    """Show info about an image"""

    # Get the image and user information
    image = crud.get_image_by_id(image_id)
    user = crud.get_user_by_email(session.get("user_email"))
    user_id = user.user_id
    logged_in_email = session.get("user_email")

    # Get the likes and comments for a particular image
    like_count = len(crud.get_likes_by_image_id(image_id))
    comments = crud.get_comment_by_image_id(image_id = image.image_id)

    # Check that the user is logged in, if so, show them the image details
    if logged_in_email is None:
        flash("Sorry! You need to be logged in before you can add a comment!")

    else:
        user = crud.get_user_by_email(logged_in_email)
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
    if image and "user_email" in session:

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

    if session["user_email"] != None:
        
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
    if user_zip != None:
        username = user_zip.username
        instagram = user_zip.instagram
        twitter = user_zip.twitter
        tiktok = user_zip.tiktok
        website = user_zip.website
        art_collection = user_zip.artist_collection


        return render_template('user-profile.html',
                                zipcode=zipcode,
                                user_zip=user_zip,
                                username=username,
                                instagram=instagram,
                                twitter=twitter,
                                tiktok=tiktok,
                                website=website,
                                art_collection=art_collection)
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
                                zipcode=zipcode,
                                username=username,
                                instagram=instagram,
                                twitter=twitter,
                                tiktok=tiktok,
                                website=website,
                                art_collection=art_collection)
        
    else:
        flash("Sorry! We can't find anyone random right now. Try again later.")
        return redirect("/zipcode_input")


@app.route("/load_art_show")
def load_art_show():
    """Show a random piece of art posted on the platform"""

    # Get the user that is currently logged in
    user_logged_in = session.get("user_email")

    # Query for a random user not logged in from the database
    random_user = choice(crud.get_all_not_logged_in_users(user_logged_in))

    # Get the email for our random user object
    random_users_email = random_user.email

    # Make sure that the random user is not the same as the user logged in
    if user_logged_in != random_users_email and session["user_email"]:
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
                            art_show_user=art_show_user,
                            username=username,
                            zipcode=zipcode,
                            instagram=instagram,
                            tiktok=tiktok,
                            twitter=twitter,
                            website=website,
                            art_collection=art_collection)


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
    if gallery_title != None and gallery_description != None:
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
    if image_link != None and image_title != None:

        new_image = crud.create_image(image_title, image_link, date_uploaded, artist_collection)
        db.session.add(new_image)
        db.session.commit()

        return redirect("/user_profile")
    else:
        return render_template('upload-image.html')


if __name__ == "__main__":

    import sys
    # Code to run the selenium tests in the terminal 
    if sys.argv[-1] == "selenium_test":
        connect_to_db(app, "postgresql:///testdb")
    
    # Code to run the jasmine tests in the terminal 
    elif sys.argv[-1] == "jstest":
        #connect_to_db(app, "postgresql://testdb")
        JS_TESTING_MODE = True 

    # Otherwise, run the server normally 
    else:
        connect_to_db(app)

    app.run(host="0.0.0.0", debug=True)