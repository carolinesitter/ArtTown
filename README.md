# ArtTown

## Summary

**ArtTown** is a practical and versatile app designed to offer users the ability to search for fellow artists within their area. With Art Town, users can create an account, upload content, and interact with the artwork provided by their neighboring creatives.


## About the Developer
**ArtTown** was created by Caroline Sitter. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/caroline-sitter-385a11219/).


## Technologies
### Tech Stack:
* Python
* Flask
* SQL Alchemy
* Javascript
* AJAX
* Python Unittest with Flask
* Selenium End to End Testing
* Jinja2
* HTML5
* CSS
* Cloudinary API

**ArtTown** is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. The front-end templating uses Jinja2, the HTML was built using Bootstrap, and the Javascript uses AJAX to interact with the backend. The images are uploaded and rendered through the use of the Cloudinary API. Server routes are tested using the Python unittest module. Likewise, the overall site functionality is tested with Selenium.


## Features
Upon reaching **ArtTown**, users are able to create an account (while existing users can log in). New users are asked to input information such as their desired username and password, as well as contact information such as their email and zip code. Other inputs, such as social media tags or website URL’s are optional.

![](static/img/GIFS/1.GIF)

Once a user has created their account (or logged in to their existing account) they will be directed to their profile page. Once signed in, users are granted several options in the navigation bar: Home, Search, Art Show, Explore, and Sign Out. The Home route is where the user can edit and update their user profile.

![](static/img/GIFS/2.GIF)

Here, users can upload Artist Collections where they can upload images of their work and explain the concepts behind their artistic visions. Users can also click on their images to check up on the engagement other users have with their content. If a user would like to add, remove, or edit their original post, they are able to do so by clicking the “Edit” and “Add Image” buttons below each of their collections. 

![](static/img/GIFS/3.GIF)

The next feature that the user can navigate to is the Search tab. Here, users are presented with two options: "Search by Zipcode" or "Randomize". When an artist chooses to search by zipcode, they are then shown a random profile of a user with the matching zipcode. Likewise, when a user decides to randomize their search entirely, they are shown a new profile of a user regardless of their zipcode.

![](static/img/GIFS/4.GIF)

When an artist navigates to the explore tab, they are presented with a grid of clickable images that they can interact with. Users are able to like, comment, and visit the profile pages of others who have left comments on said post. Users are also able to like/unlike, as well as edit, delete, and save their comments on the image in question.

![](static/img/GIFS/5.GIF)

The Art Show is a feature which allows users to view a random Art Gallery from another user on the site. Here, the user is able to view the gallery and also navigate to the artist’s profile page to collect their contact information. 

![](static/img/GIFS/6.GIF)

Lastly, users can log out and delete their session by simply clicking the "Sign Out" option in the navigation menu. 

![](static/img/GIFS/7.GIF)


## For Version 2.0

* Follow/Unfollow: users would be able to have a list of artists that they would like to follow and keep up with.
* A Post Feed: users can exclusively keep up with the latest posts from the artists they follow.
* Password Hashing: passwords will be hashed before they are saved to the database.

## Installation

### To run **ArtTown**:

1.) Install PostgreSQL (Mac OSX).

2.) Fork this repository.

3.) Then, clone this repo in your terminal.

```
git clone https://github.com/carolinesitter/ArtTown.git
```

4.) Create and activate a virtual environment inside of your **ArtTown** directory.

```
virtualenv env
source env/bin/activate
```

5.) Install the dependencies.

```
pip install -r requirements.txt
```

6.) Sign up to use the [Cloudinary API](https://cloudinary.com/).

7.) Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export CLOUDINARY_KEY="YOUR_SECRET_KEY"
export CLOUDINARY_SECRET="YOUR_SECRET_KEY"
```

8.) You can also save a secret key and add it to <kbd>secrets.sh</kbd>:

```
export SECRET_KEY="YOUR_SECRET_KEY"
```

9.) Source your keys from your <kbd>secrets.sh</kbd> file into your virtual environment.

```
source secrets.sh
```

10.) Set up the database:

```
createdb artists-by-zip
python -i model.py
>>> db.create_all()
psql artists-by-zip < demodata.sql
```

Run the app:

```
python3 server.py
```

You can now navigate to "localhost:5000/" to access **ArtTown**.

## Testing with Flask

1.) After completing the installation requirements for **ArtTown**, navigate to your terminal window.

2.) You can run the tests with Flask by typing:

```
python3 tests.py
```

3.) You can also run the tests in verbose mode by typing:

```
python3 tests.py -v
```

## Testing with Selenium

1.) Before testing **ArtTown** with Selenium, check your terminal windows to ensure that you are **not** actively running the regular **ArtTown** server.

2.) Ensure that you have at least two terminal windows open, in the **ArtTown** directory, and running the virtual environment.

3.) In one terminal, type the following command to run the **ArtTown** server with Selenium:

```
python3 server.py selenium_test
```

4.) In the other terminal, type the following command to run the Selenium tests.

```
python3 selenium_tests.py
```

5.) Similar to testing with Flask, you can also run the Selenium tests in verbose mode by typing:

```
python3 selenium_tests.py -v
```