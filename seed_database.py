"""Script to seed database. Make test users and data.
    TODO: pull in media info via json for database."""

import os
import json
from faker import Faker
from random import choice, randint

import crud
import model
import server
import secrets

os.system('dropdb library')
os.system('createdb library')
os.system('source secrets.sh')

model.connect_to_db(server.app, echo=False)
model.db.create_all()

fake = Faker()

# create test data:
for new_type in ['book', 'movie', 'tv']:
    crud.create_media_type(new_type)

## Open Library API version:
# with open('data/test_books.json') as f:
#     book_data = json.loads(f.read())
# books_in_db = []
# for book in book_data['entries']:
#     title, cover_image = (book['title'], book['picture']['url'])
#     new_book = crud.create_book(title=title, type_id=1, author='somebody', cover=cover_image)
#     books_in_db.append(new_book)

## Google Books API version:
with open('data/books.json') as f:
    book_data = json.loads(f.read())
books_in_db = []
for book in book_data['items']:
    # genres = book['categories'] # TODO: assign these now!
    new_book = crud.create_book(title=book['volumeInfo']['title'], 
                                type_id=1, 
                                author=book['volumeInfo']['authors'][0], 
                                description=book['volumeInfo'].get('description'), # NOTE: The Hobbit has no description...
                                cover=book['volumeInfo']['imageLinks'].get('thumbnail'),
                                pages=book['volumeInfo'].get('pageCount'))
                                # year=book['volumeInfo']['publishedDate'], # TODO: add this to model
                                # isbn=book['volumeInfo']['industryIdentifiers']['ISBN_13']) # TODO: figure out how to unpack this.
    books_in_db.append(new_book)

# cosmos = crud.create_item(title='Cosmos', type_id=1)
contact = crud.create_book(title='Contact', type_id=1, author='Carl Sagan', pages=434)
sunshine = crud.create_movie(title='Sunshine', type_id=2, length=107, year=2007)
sg1_ep1 = crud.create_tv_ep(title='Children of the Gods', type_id=3, 
                        show_title='Stargate SG-1', ep_length=92, season=1)

sources = ['owned', 'library', 'amazon']

# create test users:
bob = crud.create_user(fname='bob', lname='bobson', email='bob@bob.com', pwd='bob')
for i in range(10):
    new_user = crud.create_user(fname=fake.first_name(), 
                                lname=fake.last_name(), 
                                email=fake.email(), 
                                pwd=fake.password())
    for j in range(5):
        crud.store_media_in_user_library(user=new_user, 
                                        media_item=choice(books_in_db), 
                                        rating=randint(1,5), 
                                        review=fake.text(), 
                                        source=choice(sources))

# create & assign genres:
sci = crud.create_genre(genre_name = 'Science')
scifi = crud.create_genre(genre_name = 'Science Fiction')

# crud.assign_genre(cosmos, sci)
crud.assign_genre(contact, scifi)
crud.assign_genre(sunshine, scifi)
crud.assign_genre(sg1_ep1, scifi)

# assign user-specific media:
# crud.store_media_in_user_library(user=bob, media_item=cosmos, rating=5, 
                        # review='We are all starstuff.', source='owned')
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

# user update:
bob_cosmos_update = crud.create_user_update(bob, contact, update_value=50)
