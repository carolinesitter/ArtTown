"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb artists-by-zip")

os.system('createdb artists-by-zip')

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


    db_user = crud.create_user(first_name, last_name, username, email,
                                password, instagram, twitter, tiktok,
                                website, zipcode)

    users_in_db.append(db_user)

    model.db.session.add_all(users_in_db)

#load artist collection data from json file

with open('data/artist-collection.json') as f:
    artist_collection_data = json.loads(f.read())

artist_collection_in_db = []

for collection in artist_collection_in_db:
    gallery_title = collection['gallery_title']
    gallery_description = collection['gallery_description']

    db_collection = crud.create_artist_collection(gallery_title, gallery_description)

    artist_collection_in_db.append(db_collection)

    model.db.session.add_all(artist_collection_in_db)


#load image data from json file

with open('data/images.json') as f:
    image_data = json.loads(f.read())

images_in_db = []

for image in images_in_db:
    image_title = image['image_title']
    image_link = image['image_link']

    date_uploaded = datetime.strptime(image['date_uploaded'], "%M-%d-%y")

    db_image = crud.create_image(image_title, image_link, date_uploaded)

    users_in_db.append(db_image)

model.db.session.add_all(images_in_db)



model.db.session.commit()




