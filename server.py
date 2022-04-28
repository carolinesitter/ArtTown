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
    
    return render_template('homepage.html')

###########

# CREATE PROFILE AND REGISTER TO DATABASE

###########

@app.route("/register_profile", methods=["POST"])
def register_profile():
    """Check if account has already been created,
        if not, create new account and add user to db"""
    
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

    user = crud.get_user_by_email(email)
    
    if user:
        flash("User already registered. Please log in.")
    
    # elif password != verify_password:
    #     flash("Sorry! Your passwords do not match. Please try again.")

    else:
        user = crud.create_user(first_name, last_name, username, email,
                password, instagram, twitter, tiktok, website, zipcode)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! Your account has been created. You may now log in!")

    return redirect("/")        

###########

# LOG IN ROUTE

###########

@app.route("/log_in", methods=["POST"])
def user_login():
    """Log a user in"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

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

    session['user_email'] = None

    return redirect("/")

###########

# CREATE PROFILE FORM 

###########

@app.route("/create_profile")
def create_profile():
    """Create a new profile"""

    return render_template('create-profile.html')

###########

# SHOW USER PROFILE

###########

@app.route("/user_profile")
def user_profile():
    """Show user_profile"""

    if "user_email" in session:

        email = session['user_email']
        user = crud.get_user_by_email(email)

        username = user.username
        zipcode = user.zipcode
        instagram = user.instagram
        tiktok = user.tiktok
        twitter = user.twitter
        website = user.website
        art_collection = user.artist_collection

        return render_template('user-profile.html',
                                username=username,
                                zipcode=zipcode,
                                instagram=instagram,
                                tiktok=tiktok,
                                twitter=twitter,
                                website=website,
                                art_collection=art_collection)

    else:
        redirect("/")


###########

# SHOW IMAGE DETAILS

###########


@app.route("/user_profile/<image_id>/comments", methods=["GET"])
def show_image_info(image_id):
    """Show info about an image when link is clicked"""

    image = crud.get_image_by_id(image_id)
    logged_in_email = session.get("user_email")

    #get likes and comments

    like_count = len(image.likes)

    comments = crud.get_comment_by_image_id(image_id = image.image_id)

    if logged_in_email is None:
        flash("Sorry! You need to be logged in before you can add a comment!")

    else:
        user = crud.get_user_by_email(logged_in_email)
        return render_template('image_details.html',
                                user=user, 
                                image=image, 
                                like_count=like_count,
                                comments=comments)


###########

# ADD A COMMENT

###########


@app.route("/user_profile/<image_id>/comments", methods=["POST"])
def add_new_comment(image_id):
    """Allow users to add a comment"""

    comment = request.json.get("new_comment")

    image = crud.get_image_by_id(image_id)


    if (comment != None) and (image != None) and ("user_email" in session):
        
        user = crud.get_user_by_email(session.get("user_email"))
        user_id = user.user_id
        image_id = image.image_id
        username = user.username

        #crud_comment_test = crud.create_comment(comment, user_id, image_id)
        image.comments.append(crud.create_comment(comment, image_id, user_id))

        db.session.add(image) 
        db.session.commit()

        return jsonify({"status": "OK", "username": username,"comment": comment})

    else:
        return jsonify({"status": "FAILED"})


###########

# LIKE AN IMAGE 

###########


@app.route("/api/user_profile/<image_id>/likes")
def like_an_image(image_id):
    """Allows users to like an image"""

    image = crud.get_image_by_id(image_id)

    # verify that a user hasn't already liked a post ?


    # user = crud.get_user_by_email(session.get("user_email"))
    # user_id = user.user_id
    # like = crud.get_likes_info(image_id, user_id)

    # if like != None:
    #     flash("Don't Worry! You have already liked this image!")


    if image and "user_email" in session:
        
        user = crud.get_user_by_email(session.get("user_email"))
        user_id = user.user_id

        # image_id = image.image_id
        #like = crud.get_likes_info(image_id, user_id)

        image.likes.append(crud.create_like(len(image.likes) + 1, image_id, user_id))
        
        db.session.add(image) 
        db.session.commit()

        return jsonify({"status": "OK", "like_count": len(image.likes)})

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