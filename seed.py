"""Script to seed initial sample database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb artists-by-zip")

os.system('createdb artists-by-zip')

#automatically reads in the sql file into the database
#os.system('psql artists-by-zip < sampledata.sql')

model.connect_to_db(server.app)
model.db.create_all() 


#load user data from json file
with open('data/user-data.json') as f:
    user_data = json.loads(f.read())

#create users, store them in list
users_in_db = []

for user in user_data:
    first_name = user['first_name']
    last_name = user['last_name']
    username = user['username']
    email = user['email']
    zipcode = user['zipcode']
    password = user['password']

    # Check if the user inputted their socials,
    # if not, return None as they are optional inputs
    if 'instagram' in user:
        instagram = user['instagram']
    else:
        instagram = None
    if 'tiktok' in user:
        tiktok = user['tiktok']
    else:
        tiktok = None
    if 'twitter' in user:
        twitter = user['twitter']
    else:
        twitter = None
    if 'website' in user:
        website = user['website']
    else:
        website = None

    # Create our new user from the JSON files and add to db
    db_user = crud.create_user(first_name, last_name, username, email,
                                password, instagram, twitter, tiktok,
                                website, zipcode)

    users_in_db.append(db_user)

    model.db.session.add_all(users_in_db)



#load artist collection data from json file
with open('data/artist-collection.json') as f:
    artist_collection_data = json.loads(f.read())

# Create an empty list that will hold the artist collections
artist_collection_in_db = []

# Create an artist collection and store it to the database
for collection in artist_collection_data:
    gallery_title = collection['gallery_title']
    gallery_description = collection['gallery_description']
    user = choice(users_in_db)

    db_collection = crud.create_artist_collection(gallery_title, gallery_description, user)

    artist_collection_in_db.append(db_collection)

    model.db.session.add_all(artist_collection_in_db)


#load image data from json file
with open('data/images.json') as f:
    image_data = json.loads(f.read())

images_in_db = []

# Create an image and add it to the database
for image in image_data:
    image_title = image['image_title']
    image_link = image['image_link']
    artist_collection = choice(artist_collection_in_db)


    date_uploaded = datetime.strptime(image['date_uploaded'], "%Y-%m-%d")

    db_image = crud.create_image(image_title, image_link, date_uploaded, artist_collection)

    images_in_db.append(db_image)

model.db.session.add_all(images_in_db)



model.db.session.commit()




