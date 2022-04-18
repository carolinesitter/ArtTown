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

#CREATE USER PROFILE AND MAKE SURE ONLY ONE EXISTS PER EMAIL

# @app.route("/create_profile")
# def create_profile():
#     """Check if account has already been created"""
    
#     email = request.form.get("email")
#     password = request.form.get("password")
#     user = crud.get_user_by_email(email)
    
#     if user:
#         flash("User already registered")
#     else:
#         user = crud.create_user(email, password)
#         db.session.add(user)
#         db.session.commit()
#         flash("User created successfully; you may now log in")
    
#     return redirect("/user_profile")        
    

# add another create profile app route with POST 
# -- to add and store info to db and sessions

#CREATE USER LOG IN ROUTE
# @app.route("/login", methods=["POST"])
# def user_login():
#     """Log a User in"""

#     email = request.form.get("email")
#     password = request.form.get("password")
    # user = crud.get_user_by_email(email)

    # if not user or user.password != password:
    #     flash("Invalid email or password. Please try again.")
    #     return redirect("/")
    # else:
    #     session['user_email'] = user.email
    #     flash("Successfully logged in!")

    # return redirect("/user_profile")
    
    

@app.route("/user_profile")
def user_profile():
    """Show user_profile"""

    return render_template('user-profile.html')


@app.route("/rand_user_profile")
def rand_user_profile():
    """Show Random User Profile from Data"""

    return render_template('rand-user-profile.html')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)