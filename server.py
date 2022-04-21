"""Server for artist by zipcode app"""

from flask import (Flask, render_template, request, flash, session,
                redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage"""
    
    return render_template('homepage.html')

###########

# CREATE USER PROFILE AND MAKE SURE ONLY ONE EXISTS PER EMAIL:

@app.route("/register_profile", methods=["POST"])
def register_profile():
    """Check if account has already been created,
        if not, create new account and add user to db"""
    
    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    instagram = request.form.get("instagram")
    twitter = request.form.get("twitter")
    tiktok = request.form.get("tiktok")
    website = request.form.get("website")
    zipcode = request.form.get("zipcode")

    user = crud.get_user_by_email(email)
    
    if user:
        flash("User already registered. Please log in.")

    else:
        user = crud.create_user(first_name, last_name, username, email,
                password, instagram, twitter, tiktok, website, zipcode)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! Your account has been created. You may now log in!")

    return redirect("/")        
    

# add another create profile app route with POST 
# -- to add and store info to db and sessions

###########

# CREATE USER LOG IN ROUTE
@app.route("/log_in", methods=["POST"])
def user_login():
    """Log a user in"""

    # username = request.form.get("username")
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

@app.route("/create_profile")
def create_profile():
    """Create a new profile"""

    return render_template('create-profile.html')
    

@app.route("/user_profile")
def user_profile():
    """Show user_profile"""

    email = session['user_email']

    user = crud.get_user_by_email(email)

    username = user.username
    zipcode = user.zipcode
    instagram = user.instagram
    tiktok = user.tiktok
    twitter = user.twitter
    website = user.website

    return render_template('user-profile.html',
                            username=username,
                            zipcode=zipcode,
                            instagram=instagram,
                            tiktok=tiktok,
                            twitter=twitter,
                            website=website)

@app.route("/zipcode_input")
def zipcode_input():
    """Show input box where artists can type in zip code"""

    return render_template('search-by-zip.html')

@app.route("/search_by_zipcode", methods=["POST"])
def search_by_zipcode():
    """Enter in zipcode, render random user profile"""

    # get zip from inputs, check if it equals a zip from data.json

    zipcode = int(request.form.get("zipcode"))
    user_zip = crud.get_user_by_zipcode(zipcode)
    print(user_zip)
    if user_zip != None:
        fake_username = user_zip.username
        fake_zipcode = user_zip.zipcode
        fake_instagram = user_zip.instagram
        fake_twitter = user_zip.twitter
        fake_tiktok = user_zip.tiktok
        fake_website = user_zip.website
        fake_art = user_zip.artist_collection


        return render_template('rand-user-profile.html',
                                zipcode=zipcode,
                                user_zip=user_zip,
                                fake_username=fake_username,
                                fake_zipcode=fake_zipcode,
                                fake_instagram=fake_instagram,
                                fake_twitter=fake_twitter,
                                fake_tiktok=fake_tiktok,
                                fake_website=fake_website,
                                fake_art=fake_art)
    else:
        flash("Sorry! No results match the Zip Code you entered. Please try again!")
        return redirect('/zipcode_input')



@app.route("/create_post_form")
def create_new_post():
    """Render template for artists to upload images to their profile"""

    return render_template('create-post.html')

###########

# ADD IMAGE TO PROFILE:

@app.route("/create_new_post", methods=["POST"])
def upload_new_post():
    """Allow artists to upload images onto profile,
    redirect to user profile once submitted"""

    # implement cloudinary, reference documentation
    # this may be where you will need AJAX?

    # may need to implement cloudinary in user_profile route!

    return redirect("user-profile.html")

###########

# SHOW USER IMAGE ON CLICK:

# @app.route("/user_profile.html/<user_image>")
# def show_user_image():
#     """When you click on an image's link,
#     render a page with the image and its info"""

#     image = crud.get ....

#     return render_template('user-image-details.html', image=image)

###########

# SHOW RANDOM USER IMAGE ON CLICK:

# @app.route("/rand_user_profile/<sample_image>")
# def show_rand_user_image():
#     """When you click on a random user's image link,
#     render a page with the image and its info"""

#     rand_user_image = crud.get ....

#     return render_template('rand-user-image.html',
#                             rand_user_image = rand_user_image)

###########


# @app.route("/rand_user_profile")
# def rand_user_profile():
#     """Show Random User Profile from Data"""

#     fake_username = crud.get_user_by_username(username)
#     fake_zipcode = crud.get_user_by_zipcode(zipcode)
#     fake_instagram = crud.get_user_by_instagram(instagram)
#     fake_twitter = crud.get_user_by_twitter(twitter)
#     fake_tiktok = crud.get_user_by_tiktok(tikok)
#     fake_website = crud.get_user_by_website(website)


#     return render_template('rand-user-profile.html',
#                             fake_username=fake_username,
#                             fake_zipcode=fake_zipcode,
#                             fake_instagram=fake_instagram,
#                             fake_twitter=fake_twitter,
#                             fake_tiktok=fake_tiktok,
#                             fake_website=fake_website)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)