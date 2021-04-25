"""Script to seed database. Make test users and data.
    TODO: pull in media info via json for database."""

import os
import json
from faker import Faker
from random import choice, randint, random
from datetime import datetime, date, time

import crud
import model
import server

os.system('dropdb library')
os.system('createdb library')

model.connect_to_db(server.app, echo=False)
model.db.create_all()

fake = Faker()

# get random start date
def random_date(earliest_date):
    """ Get a random date for seeding purposes. """

    return earliest_date + (date.today() - earliest_date) * random()


# create test data:
books_in_db = []
movies_in_db = []
tv_in_db = []

# create types
for new_type in ['book', 'movie', 'tv', 'podcast', 'game', 'comic', 'other']:
    crud.create_media_type(new_type)

# create genres:
for new_genre in ['Science', 'Fiction', 'Nonfiction']:
    crud.create_genre(new_genre)
scifi = crud.create_genre(genre_name = 'Science Fiction')
clifi = crud.create_genre(genre_name = 'Climate Fiction')

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

    if book['volumeInfo'].get('categories'):
        for genre in book['volumeInfo']['categories']:
            new_genre = crud.create_genre(genre.title())
            crud.assign_genre(new_book, new_genre)

    books_in_db.append(new_book)

## IMDB API for movies:
with open('data/movies.json') as f2:
    movie_data = json.loads(f2.read())

for movie in movie_data['items']:
    new_movie = crud.create_movie(title=movie['title'], 
                                type_id=2,
                                cover=movie['image'],
                                description=movie['plot'],
                                length=movie['runtimeMins'],
                                year=movie['year'])

    if movie.get('genreList'):
        for genre in movie['genreList']:
            new_genre = crud.create_genre(genre['key'].title())
            crud.assign_genre(new_movie, new_genre)

    movies_in_db.append(new_movie)

## IMDB API for TV:
with open('data/tv.json') as f3:
    tv_data = json.loads(f3.read())

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

sources = ['owned', 'library', 'amazon', 'other']

# create test users:
bob = crud.create_user(fname='bob', lname='bobson', email='bob@bob.com', pwd='bob', profile_pic='https://images.gr-assets.com/authors/1406058780p8/3089156.jpg')
rose = crud.create_user(fname='rose', lname='tyler', email='rose@tardis.com', pwd='badwolf', profile_pic='https://bit.ly/3fPVcfn')
wendy = crud.create_user(fname='Wendy', lname='Carter', email='wcarter@dontstarve.com', pwd='abigail', profile_pic='/static/images/wendy_pf.png')
leslie = crud.create_user(fname='Leslie', lname='Knope', email='lknope@pawnee.com', pwd='lilsebastian', profile_pic='https://media.glamour.com/photos/569580c38fa134644ec26260/master/pass/entertainment-2015-01-leslie-knope-final-season-main.jpg') 
william = crud.create_user(fname='William', lname='Adama', email='adama@bsg.com', pwd='sosayweall', profile_pic='https://cdn.quotesgram.com/img/50/90/1225779377-admiral-adama-one_288x288.jpg')
daniel = crud.create_user(fname='Daniel', lname='Jackson', email='djackson@sgc.com', pwd="share", profile_pic='https://tse2.mm.bing.net/th?id=OIP.W8baHOdXLIJsdi4V46xR-wHaLD&pid=Api')
buffy = crud.create_user(fname='Buffy', lname='Summers', email='buffy@summers.com', pwd='mrpointy', profile_pic='https://tse1.mm.bing.net/th?id=OIP.b3ngjS5r4_W4nFmetfqDGQHaFf&pid=Api')
test_users = [bob, rose, wendy, leslie, william, daniel, buffy]

# assign media
reviews = ['WOOOO','This was the beeest!','meh...','Super interesting concept.','This totally broke my heart.']
for user in test_users: 
    user_media = []
    earliest_date = date(2010, 1, 1)
    for j in range(5):
        item_choice = choice(books_in_db)
        if item_choice not in user_media:
            user_media.append(item_choice)
            start_date = random_date(earliest_date)
            # TODO: weight start/end_dates to usually be within a year of each other
            end_date = random_date(start_date)
            crud.store_media_in_user_library(user=user, 
                                            media_item=item_choice, 
                                            rating=randint(1,5), 
                                            review=choice(reviews), 
                                            source=choice(sources),
                                            start_date=start_date,
                                            end_date=end_date,
                                            dnf=False)
    for n in range(2):
        item_choice = choice(movies_in_db)
        if item_choice not in user_media:
            user_media.append(item_choice)
            start_date = random_date(earliest_date)
            crud.store_media_in_user_library(user=user, 
                                            media_item=item_choice, 
                                            rating=randint(1,5), 
                                            review=choice(reviews), 
                                            source=choice(sources),
                                            start_date=start_date,
                                            end_date=start_date,
                                            dnf=False)
    for m in range(1):
        item_choice = choice(tv_in_db)
        user_media.append(item_choice)
        start_date = random_date(earliest_date)
        crud.store_media_in_user_library(user=user,
                                        media_item=item_choice,
                                        rating=randint(1,5),
                                        review=choice(reviews),
                                        source=choice(sources),
                                        start_date=start_date,
                                        end_date=start_date,
                                        dnf=False)


# assign genres:
# crud.assign_genre(cosmos, sci)
crud.assign_genre(contact, scifi)
crud.assign_genre(mononoke, clifi)
crud.assign_genre(sg1_ep1, scifi)

# assign user-specific media: # TODO: include dates too!
# crud.store_media_in_user_library(user=bob, media_item=cosmos, rating=5, 
                        # review='We are all starstuff.', source='owned')
crud.store_media_in_user_library(user=rose, media_item=contact, rating=5, 
                        review='woot', source='owned', 
                        start_date=random_date(date(2015,1,1)))
adate=random_date(date(2015,1,1))
crud.store_media_in_user_library(user=rose, media_item=mononoke, rating=5, 
                        review='beautiful soundtrack and movie', source='library', 
                        start_date=adate, end_date=adate)
adate=random_date(date(2015,1,1))
crud.store_media_in_user_library(user=rose, media_item=sg1_ep1, rating=4, 
                        review='That was a long pilot.', source='amazon', 
                        start_date=adate, end_date=adate)

# organize collections:
favorites = crud.create_collection(user=rose, collection_name='Favorites')

crud.assign_to_collection(rose, contact, favorites)
crud.assign_to_collection(rose, mononoke, favorites)
crud.assign_to_collection(rose, sg1_ep1, favorites)

# user update:
rose_contact_update = crud.create_user_update(rose, contact, update_value=50)

