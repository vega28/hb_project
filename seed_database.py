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
                                pages=book['volumeInfo'].get('pageCount'),
                                year=book['volumeInfo'].get('publishedDate')) 
                                # isbn=book['volumeInfo']['industryIdentifiers']['ISBN_13']) # TODO: figure out how to unpack this.
    books_in_db.append(new_book)

## IMDB API for movies:
with open('data/movies.json') as f2:
    movie_data = json.loads(f2.read())
movies_in_db = []
for movie in movie_data['items']:
    new_movie = crud.create_movie(title=movie['title'], 
                                type_id=2,
                                cover=movie['image'],
                                description=movie['plot'],
                                length=movie['runtimeMins'],
                                year=movie['year'])
    movies_in_db.append(new_movie)

## IMDB API for TV:
with open('data/tv.json') as f3:
    tv_data = json.loads(f3.read())
tv_in_db = []
for ep in tv_data['items']:
    new_ep = crud.create_tv_ep(title=ep['title'], 
                                type_id=3,
                                cover=ep['image'],
                                description=ep['plot'],
                                show_title=ep['tvEpisodeInfo']['seriesTitle'],
                                season=ep['tvEpisodeInfo']['seasonNumber'],
                                ep_of_season=ep['tvEpisodeInfo']['episodeNumber'],
                                ep_length=ep['runtimeMins'],
                                year=ep['year'])
    tv_in_db.append(new_ep)


# cosmos = crud.create_item(title='Cosmos', type_id=1,
#                             cover='http://books.google.com/books/content?id=cDKODQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
#                             description="Presents an illustrated guide to the universe and to Earth's relationship to it, moving from theories of creation to humankind's discovery of the cosmos, to general relativity, to space missions, and beyond.")
contact = crud.create_book(title='Contact', type_id=1, 
                            cover='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1567132653l/94786._SY475_.jpg',
                            description="In December, 1999, a multinational team journeys out to the stars, to the most awesome encounter in human history. Who -- or what -- is out there? \nIn Cosmos, Carl Sagan explained the universe. In Contact, he predicts its future -- and our own.",
                            author='Carl Sagan', 
                            pages=434)
mononoke = crud.create_movie(title='Princess Mononoke', type_id=2, 
                            cover='https://m.media-amazon.com/images/M/MV5BNGIzY2IzODQtNThmMi00ZDE4LWI5YzAtNzNlZTM1ZjYyYjUyXkEyXkFqcGdeQXVyODEzNjM5OTQ@._V1_UX182_CR0,0,182,268_AL_.jpg', 
                            description="On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony. In this quest he also meets San, the Mononoke Hime.", 
                            length=134, 
                            year=1997)
sg1_ep1 = crud.create_tv_ep(title='Children of the Gods', type_id=3, 
                            cover='https://m.media-amazon.com/images/M/MV5BMTc3MjEwMTc5N15BMl5BanBnXkFtZTcwNzQ2NjQ4NA@@._V1_UX182_CR0,0,182,268_AL_.jpg',
                            description="Colonel Jack O'Neill is brought out of retirement to lead a new expedition back to Abydos, only to find an old friend, a new enemy and a far wider use of the Stargate.",
                            show_title='Stargate SG-1', 
                            ep_length=92, 
                            season=1)

sources = ['owned', 'library', 'amazon']

# create test users:
bob = crud.create_user(fname='bob', lname='bobson', email='bob@bob.com', pwd='bob', profile_pic='https://images.gr-assets.com/authors/1406058780p8/3089156.jpg')
rose = crud.create_user(fname='rose', lname='tyler', email='rose@tardis.com', pwd='badwolf', profile_pic='https://bit.ly/3fPVcfn')
wendy = crud.create_user(fname='Wendy', lname='Carter', email='wcarter@dontstarve.com', pwd='abigail', profile_pic='/static/images/wendy_pf.png')
for i in range(10): # FIXME: currently user can have duplicate media items.
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
    for n in range(2):
        crud.store_media_in_user_library(user=new_user, 
                                        media_item=choice(movies_in_db), 
                                        rating=randint(1,5), 
                                        review=fake.text(), 
                                        source=choice(sources))
    for m in range(1):
        crud.store_media_in_user_library(user=new_user,
                                        media_item=choice(tv_in_db),
                                        rating=randint(1,5),
                                        review=fake.text(),
                                        source=choice(sources))


# create & assign genres:
sci = crud.create_genre(genre_name = 'Science')
scifi = crud.create_genre(genre_name = 'Science Fiction')
clifi = crud.create_genre(genre_name = 'Climate Fiction')

# crud.assign_genre(cosmos, sci)
crud.assign_genre(contact, scifi)
crud.assign_genre(mononoke, clifi)
crud.assign_genre(sg1_ep1, scifi)

# assign user-specific media:
# crud.store_media_in_user_library(user=bob, media_item=cosmos, rating=5, 
                        # review='We are all starstuff.', source='owned')
crud.store_media_in_user_library(user=rose, media_item=contact, rating=5, 
                        review='woot', source='owned')
crud.store_media_in_user_library(user=rose, media_item=mononoke, rating=5, 
                        review='beautiful soundtrack and movie', source='library')
crud.store_media_in_user_library(user=rose, media_item=sg1_ep1, rating=4, 
                        review='That was a long pilot.', source='prime video')

# organize collections:
favorites = crud.create_collection(user=rose, collection_name='Favorites')

crud.assign_to_collection(rose, contact, favorites)
crud.assign_to_collection(rose, mononoke, favorites)
crud.assign_to_collection(rose, sg1_ep1, favorites)

# user update:
rose_contact_update = crud.create_user_update(rose, contact, update_value=50)

