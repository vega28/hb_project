"""CRUD opertions."""

from model import *
from datetime import datetime


def create_user(fname, lname, email, pwd, profile_pic=None):
    """ Create and return a new user. """

    user = User(fname=fname, lname=lname, email=email, pwd=pwd, profile_pic=profile_pic)

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """ Query database and return a list of all users. """
    
    return User.query.all()


def get_user_by_id(user_id):
    """ Query database and return a user by their id. """

    return db.session.query(User).filter(User.user_id==user_id).first()


def get_user_by_email(email):
    """ Query database and return a user by their email. """

    return db.session.query(User).filter(User.email==email).first()


def create_media_type(type_name):
    """ Create and return a new media type. """

    new_type = Type(media_type=type_name)

    db.session.add(new_type)
    db.session.commit()   

    return new_type


def create_book(title, type_id, author, cover=None, description=None, 
                edition=None, pages=None, isbn=None):
    """ Create and return a new book. """

    new_item = Book(title=title, 
                    type_id=type_id,  # TODO: specify this automatically!
                    cover=cover, 
                    description=description, 
                    author=author, 
                    edition=edition, 
                    pages=pages, 
                    isbn=isbn)

    db.session.add(new_item)
    db.session.commit()   

    return new_item


def create_movie(title, type_id, cover=None, description=None, length=None, year=None):
    """ Create and return a new movie. """

    new_item = Movie(title=title, 
                    type_id=type_id,  # TODO: specify this automatically!
                    cover=cover, 
                    description=description, 
                    length=length, 
                    year=year)

    db.session.add(new_item)
    db.session.commit()   

    return new_item


def create_tv_ep(title, type_id, show_title, cover=None, description=None, 
                ep_length=None, season=None):
    """ Create and return a new tv episode. """

    new_item = TVEpisode(title=title, 
                        type_id=type_id,  # TODO: specify this automatically!
                        cover=cover, 
                        description=description, 
                        show_title=show_title, 
                        ep_length=ep_length, 
                        season=season)

    db.session.add(new_item)
    db.session.commit()   

    return new_item


def create_item(title, type_id, cover=None, description=None):
    """ Create and return a new generic media item. """

    new_item = Item(title=title, type_id=type_id, cover=cover, description=description)

    db.session.add(new_item)
    db.session.commit()   

    return new_item


def get_all_media():
    """ Query database and return a list of all media items. """

    return Item.query.all() 


def get_all_books():
    """ Query database and return a list of all books. """

    return Book.query.all() 


def get_item_by_id(item_id):
    """ Query database and return an item by its id. """

    return db.session.query(Item).filter(Item.item_id==item_id).first()


def get_all_movies():
    """ Query database and return a list of all movies. """

    return Movie.query.all() 


def get_all_tv():
    """ Query database and return a list of all tv episodes. """

    return TVEpisode.query.all() 


def create_genre(genre_name):
    """ Create and return a new genre. """

    new_genre = Genre(genre_name=genre_name)

    db.session.add(new_genre)
    db.session.commit()   

    return new_genre


def get_all_genres():
    """ Query database and return a list of all genres. """

    return Genre.query.all()


def assign_genre(media_item, genre):
    """ Associate the specified media item with the specified genre. 
        Return MediaGenre association object. """

    association = MediaGenre(item_id=media_item.item_id, genre_id=genre.genre_id)

    db.session.add(association)
    db.session.commit()   

    return association


def get_by_genre(genre_name, media_type=None):
    """ Query database and return a list of specified media items by genre. """

    # if media_type:
    #     filter by media_type, then filter by genre, then return list.

    # else:
    return Genre.query.filter(Genre.genre_name == genre_name).first().items


def store_media_in_user_library(user, media_item, rating, review, source):
    """ Add a media item to a user's personal library.
        Allow user to include a rating, review, etc. 
        Return UserMedia object. """

    user_item = UserMedia(user_id=user.user_id, 
                        item_id=media_item.item_id, 
                        rating=rating, 
                        review=review, 
                        created_at=datetime.now(), 
                        source=source)
    # TODO: figure out timestamp for created_at!

    db.session.add(user_item)
    db.session.commit()

    return user_item


def create_collection(user, collection_name):
    """ Create and return a new collection. """

    collection = Collection(user_id=user.user_id, name=collection_name)

    db.session.add(collection)
    db.session.commit()

    return collection


def get_user_media_id(user, media_item):
    """ Query database and return the user_media_id association between 
        a user_id and a media_item. """

    return UserMedia.query.filter(UserMedia.user_id==user.user_id, 
                    UserMedia.item_id==media_item.item_id).first().user_media_id


def assign_collection(user, media_item, collection):
    """ Associate the specified media item with the specified collection. 
        Return CollectionUserMedia association object. """

    user_media_id = get_user_media_id(user, media_item)
    association = CollectionUserMedia(collection_id=collection.collection_id, 
                            user_media_id=user_media_id)

    db.session.add(association)
    db.session.commit()   

    return association


def create_user_update(user, media_item, date=None, start_bool=False, end_bool=False, update_value=None, num_times_through=None, dnf=None):
    """ Allow user to create an update on a specific media item.
        e.g. started / finished / completed 50 pages / etc... 
        Return UserUpdate object. """

    user_update = UserUpdate(user_id=user.user_id, 
                            item_id=media_item.item_id, 
                            update_entered_at = datetime.now(), 
                            date=date, 
                            start_bool=start_bool, 
                            end_bool=end_bool, 
                            update_value=update_value,
                            num_times_through=num_times_through, 
                            dnf=dnf) 

    db.session.add(user_update)
    db.session.commit()   

    return user_update


