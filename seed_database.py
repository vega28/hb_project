"""Script to seed database. Make test users and data.
    TODO: pull in media info via json for database."""

import os

import crud
import model
import server

os.system('dropdb library')
os.system('createdb library')

model.connect_to_db(server.app, echo=False)
model.db.create_all()

# create test users:
bob = crud.create_user(fname='bob', lname='bobson', email='bob@bob.com', pwd='bob')

# create test data:
for new_type in ['book', 'movie', 'tv']:
    crud.create_media_type(new_type)

cosmos = crud.create_item(title='Cosmos', type_id=1)
contact = crud.create_book(title='Contact', type_id=1, author='Carl Sagan', pages=434)
sunshine = crud.create_movie(title='Sunshine', type_id=2, length=107, year=2007)
sg1_ep1 = crud.create_tv_ep(title='Children of the Gods', type_id=3, 
                        show_title='Stargate SG-1', ep_length=92, season=1)

# create & assign genres:
sci = crud.create_genre(genre_name = 'Science')
scifi = crud.create_genre(genre_name = 'Science Fiction')

crud.assign_genre(cosmos, sci)
crud.assign_genre(contact, scifi)
crud.assign_genre(sunshine, scifi)
crud.assign_genre(sg1_ep1, scifi)

# assign user-specific media:
crud.store_media_in_user_library(user=bob, media_item=cosmos, rating=5, 
                        review='We are all starstuff.', source='owned')
crud.store_media_in_user_library(user=bob, media_item=contact, rating=5, 
                        review='woot', source='owned')
crud.store_media_in_user_library(user=bob, media_item=sunshine, rating=5, 
                        review='SpooOOOoooky', source='library')
crud.store_media_in_user_library(user=bob, media_item=sg1_ep1, rating=4, 
                        review='That was a long pilot.', source='prime video')

# organize collections:
favorites = crud.create_collection(user=bob, collection_name='Favorites')

crud.assign_collection(bob, contact, favorites)
crud.assign_collection(bob, sunshine, favorites)
crud.assign_collection(bob, sg1_ep1, favorites)

