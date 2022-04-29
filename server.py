"""Server for artist by zipcode app"""

from flask import (Flask, render_template, request, flash, session,
                redirect, url_for, jsonify)
from model import connect_to_db, db
from datetime import datetime
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

###########

# SHOW HOMEPAGE

###########

@app.route("/")
def homepage():
    """View homepage"""
    
    # This is the homepage
    return render_template('homepage.html')

###########

# CREATE PROFILE AND REGISTER TO DATABASE

###########

@app.route("/register_profile", methods=["POST"])
def register_profile():
    """Check if account has already been created,
        if not, create new account and add user to db"""

    # Get the values from our form input when a user registers an account
    email = request.form.get("email")
    password = request.form.get("password")
    #verify_password = request.form.get("verify_password")
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
    
    # Ensure that the password and verification are the same 
    # elif password != verify_password:
    #     flash("Sorry! Your passwords do not match. Please try again.")

    else:
        user = crud.create_user(first_name, last_name, username, email,
                password, instagram, twitter, tiktok, website, zipcode)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! Your account has been created. You may now log in!")

    # Send the user back to the homepage
    return redirect("/")        

###########

# LOG IN ROUTE

###########

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
        return redirect("/")
    else:
        session['user_email'] = user.email
        session['username'] = user.username

        flash("Successfully logged in!")

    return redirect("/user_profile")

###########

# LOG OUT ROUTE

###########

@app.route("/log_out")
def user_logout():
    """Allow user to log out"""

    # When the user logs out, forget their email in sessions
    session['user_email'] = None

    # Show user back to the homepage
    return redirect("/")

###########

# CREATE PROFILE FORM 

###########

@app.route("/create_profile")
def create_profile():
    """Create a new profile"""

    # Show a new user the form to create an account
    return render_template('create-profile.html')

###########

# SHOW USER PROFILE

###########

@app.route("/user_profile")
def user_profile():
    """Show user_profile"""

    # If a user is logged in, show their profile
    if "user_email" in session:

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

    # If they are not logged in, send the user to the homepage
    else:
        redirect("/")

###########

# SHOW IMAGE DETAILS

###########

@app.route("/user_profile/<image_id>/comments", methods=["GET"])
def show_image_info(image_id):
    """Show info about an image when link is clicked"""

    image = crud.get_image_by_id(image_id)
    user = crud.get_user_by_email(session.get("user_email"))
    user_id = user.user_id
    logged_in_email = session.get("user_email")

    like_count = len(crud.get_likes_by_image_id(image_id))
    comments = crud.get_comment_by_image_id(image_id = image.image_id)

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

###########

# ADD A COMMENT

###########

@app.route("/user_profile/<image_id>/comments", methods=["POST"])
def add_new_comment(image_id):
    """Allow users to add a comment"""

    comment = request.json.get("new_comment")
    image = crud.get_image_by_id(image_id)


    print(comment)
    if (comment != None) and (image != None) and ("user_email" in session):
        
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

###########

# LIKE AN IMAGE 

###########

@app.route("/api/user_profile/<image_id>/likes")
def like_an_image(image_id):
    """Allows users to like an image"""

    image = crud.get_image_by_id(image_id)

    if image and "user_email" in session:
        
        user = crud.get_user_by_email(session.get("user_email"))
        user_id = user.user_id

        like = crud.create_like(image_id, user_id)

        
        db.session.add(like) 
        db.session.commit()

        return jsonify({"status": "OK", "like_count": len(crud.get_likes_by_image_id(image_id))})

    else:
        return jsonify({"status": "FAILED"})

###########

# UN-LIKE AN IMAGE 

###########

@app.route("/api/user_profile/<image_id>/remove_likes")
def unlike_an_image(image_id):
    """Allows users to unlike an image"""

    image = crud.get_image_by_id(image_id)

    if image and "user_email" in session:
        
        user = crud.get_user_by_email(session.get("user_email"))
        user_id = user.user_id

        delete_like = crud.delete_like_by_image_and_user_id(image_id, user_id)
        
        db.session.delete(delete_like)
        db.session.commit()

        return jsonify({"status": "OK", "like_count": len(crud.get_likes_by_image_id(image_id))})

    else:
        return jsonify({"status": "FAILED"})


@app.route("/api/user_profile/<image_id>/delete_comment", methods=["POST"])
def delete_comment(image_id):
    """Allow users to delete their own comments"""

    # Get the image by id from database
    image = crud.get_image_by_id(image_id)

    # Check if the image exists and if the user is in session
    if image and "user_email" in session:

        #Get the user information
        # user = crud.get_user_by_email(session.get("user_email"))
        # user_id = user.user_id
        # username = user.username

        # Query for the comment we would like to delete
        #delete_comment = crud.delete_comment_by_image_and_user_id(image_id, user_id)
        comment = crud.get_comment_by_id(request.json.get("comment_id"))

        # Delete the comment from our database
        db.session.delete(comment)
        db.session.commit()

        # Return jsonified comment info to user-interactions.js
        return jsonify({"status": "OK"})

    else:
        return jsonify({"status": "FAILED"})

###########

# SEARCH BY ZIPCODE FORM 

###########

@app.route("/zipcode_input")
def zipcode_input():
    """Show input box where artists can type in zip code"""

    return render_template('search-by-zip.html')

###########

# SHOW RANDOM PROFILE

###########

@app.route("/search_by_zipcode", methods=["POST"])
def search_by_zipcode():
    """Enter in zipcode, show a user profile with matching zip code"""

    zipcode = int(request.form.get("zipcode"))
    user_zip = crud.get_user_by_zipcode(zipcode)

    print('\n * 5')
    print(zipcode)
    print(user_zip)
    print('\n * 5')

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

###########

# CREATE NEW POST FORM

###########

@app.route("/create_post_form")
def create_new_post():
    """Render template for artists to upload images to their profile"""

    return render_template('create-post.html')

###########

# CREATE ART COLLECTION

###########

@app.route("/create_art_collection", methods=["POST"])
def create_art_collection():
    """Get art collection and user data from browser and add to db"""

    email = session['user_email']
    user = crud.get_user_by_email(email)

    gallery_title = request.form.get("gallery-title")
    gallery_description = request.form.get("gallery-description")

    if gallery_title != None and gallery_description != None:
        artist_gallery = crud.create_artist_collection(gallery_title, gallery_description, user)
        db.session.add(artist_gallery)
        db.session.commit()

        flash("Congratulations! You have created your gallery. Now you can add photos!")
        return render_template('upload-image.html', artist_gallery=artist_gallery)

    else:
        flash("Sorry, you must give your gallery a name and description. Please try again.")
        return render_template('create-post.html')

###########

# UPLOAD AN IMAGE WITH CLOUDINARY

###########

@app.route("/upload_image", methods=["POST"])
def process_upload_data():
    """Process form data and return the url generated by Cloudinary"""

    email = session['user_email']
    user = crud.get_user_by_email(email)
    artist_collection = crud.get_art_collection_by_id(int(request.form.get('gallery-collection')))
    image_title = request.form.get('image-title')
    date_uploaded = datetime.now()
    

    filename = request.files['filename']

    result = cloudinary.uploader.upload(filename,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME)
    image_link = result['secure_url']

    if image_link != None and image_title != None:

        new_image = crud.create_image(image_title, image_link, date_uploaded, artist_collection)
        db.session.add(new_image)
        db.session.commit()

        return redirect("/user_profile")
    else:
        return render_template('upload-image.html')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)