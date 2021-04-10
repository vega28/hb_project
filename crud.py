"""CRUD opertions."""

from model import *
from datetime import datetime


def create_user(fname, lname, email, pwd, profile_pic=None):
    """ Create and return a new user. 
    e.g.

        >>> create_user(fname='rose', lname='tyler', email='rose@tardis.com', pwd='doctorwho', profile_pic='https://bit.ly/3fPVcfn')
        <User fname=Rose lname=Tyler>

    """

    check_user = User.query.filter(User.email==email).first()

    if check_user: # user already exists!
        return check_user

    else:
        user = User(fname=fname.title(), 
                    lname=lname.title(), 
                    email=email.lower(), 
                    pwd=pwd, 
                    profile_pic=profile_pic)

        db.session.add(user)
        db.session.commit()

        return user


def get_all_users():
    """ Query database and return a list of all users. """
    
    return User.query.all()


def get_user_by_id(user_id):
    """ Query database and return a user by their id. 
    e.g.
        >>> get_user_by_id(1)
        <User fname=Bob lname=Bobson>
    """

    return db.session.query(User).filter(User.user_id==user_id).first()


def get_user_by_email(email):
    """ Query database and return a user by their email. 
    e.g.
        >>> get_user_by_email('rose@tardis.com')
        <User fname=Rose lname=Tyler>
    """

    return db.session.query(User).filter(User.email==email).first()


def create_media_type(type_name):
    """ Create and return a new media type. 
    e.g.
        >>> create_media_type('book')
        <Type media_type=book type_id=1>
    """

    check_type = Type.query.filter(Type.media_type==type_name).first()

    if check_type: # media type already exists!
        return check_type

    else:
        new_type = Type(media_type=type_name)

        db.session.add(new_type)
        db.session.commit()   

        return new_type


def create_book(title, type_id, author, cover=None, description=None, 
                year=None, edition=None, pages=None, isbn=None):
    """ Create and return a new book. 
    e.g.
        >>> create_book(title='Contact', type_id=1,
        ... cover='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1567132653l/94786._SY475_.jpg',
        ... description="In December, 1999, a multinational team journeys out to the stars, to the most awesome encounter in human history. Who -- or what -- is out there? In Cosmos, Carl Sagan explained the universe. In Contact, he predicts its future -- and our own.",
        ... author='Carl Sagan', 
        ... pages=434)
        <Book title=Contact author=Carl Sagan>
    """

    new_item = Book(title=title, 
                    type_id=type_id,  # TODO: specify this automatically!
                    cover=cover, 
                    description=description,
                    # year=year, # TODO: parse year from publishedDate (which has a flexible format...)
                    author=author, 
                    edition=edition, 
                    pages=pages, 
                    isbn=isbn)

    db.session.add(new_item)
    db.session.commit()   

    return new_item


def create_movie(title, type_id, cover=None, description=None, length=None, 
                year=None):
    """ Create and return a new movie. 
    e.g.
        >>> create_movie(title='Princess Mononoke', type_id=2, 
        ... cover='https://m.media-amazon.com/images/M/MV5BNGIzY2IzODQtNThmMi00ZDE4LWI5YzAtNzNlZTM1ZjYyYjUyXkEyXkFqcGdeQXVyODEzNjM5OTQ@._V1_UX182_CR0,0,182,268_AL_.jpg', 
        ... description="On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony. In this quest he also meets San, the Mononoke Hime.", 
        ... length=134, 
        ... year=1997)
        <Movie title=Princess Mononoke year=1997>
    """

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
                year=None, ep_length=None, season=None, ep_of_season=None):
    """ Create and return a new tv episode. 
    e.g.
        >>> create_tv_ep(title='Children of the Gods', type_id=3, 
        ... cover='https://m.media-amazon.com/images/M/MV5BMTc3MjEwMTc5N15BMl5BanBnXkFtZTcwNzQ2NjQ4NA@@._V1_UX182_CR0,0,182,268_AL_.jpg',
        ... description="Colonel Jack O'Neill is brought out of retirement to lead a new expedition back to Abydos, only to find an old friend, a new enemy and a far wider use of the Stargate.",
        ... show_title='Stargate SG-1', 
        ... ep_length=92, 
        ... season=1)
        <TVEpisode show_title=Stargate SG-1 title=Children of the Gods>
    """

    new_item = TVEpisode(title=title, 
                        type_id=type_id,  # TODO: specify this automatically!
                        cover=cover, 
                        description=description, 
                        year=year,
                        show_title=show_title, 
                        ep_length=ep_length, 
                        ep_of_season=ep_of_season,
                        season=season)

    db.session.add(new_item)
    db.session.commit()   

    return new_item


def create_item(title, type_id, cover=None, description=None, year=None):
    """ Create and return a new generic media item. 
    e.g.
        >>> create_item(title='Cosmos', type_id=1,
        ... cover='http://books.google.com/books/content?id=cDKODQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
        ... description="Presents an illustrated guide to the universe and to Earth's relationship to it, moving from theories of creation to humankind's discovery of the cosmos, to general relativity, to space missions, and beyond.")
        <Media Item title=Cosmos>
    """

    new_item = Item(title=title, 
                    type_id=type_id, 
                    cover=cover, 
                    description=description,
                    year=year)

    db.session.add(new_item)
    db.session.commit()   

    return new_item


def get_all_media():
    """ Query database and return a list of all media items. """

    return Item.query.all() 


def get_all_books():
    """ Query database and return a list of all books. """

    return Book.query.all() 


def get_all_movies():
    """ Query database and return a list of all movies. """

    return Movie.query.all() 


def get_all_tv():
    """ Query database and return a list of all tv episodes. """

    return TVEpisode.query.all() 


def get_item_by_id(item_id):
    """ Query database and return an item by its id. """

    return Item.query.filter(Item.item_id==item_id).first()


def get_items_by_title(title):
    """ Query database and return a list of items with the given title. """

    return Item.query.filter(Item.title==title).all()
    

def search_db(query_terms):
    """ Query database and return a list of items that match all the given 
        search terms. Search terms should be given in dict format. """
    
    new_query = Item.query
    if query_terms.get('title'):
        new_query = new_query.filter(Item.title == query_terms['title'])
    if query_terms.get('year'):
        new_query = new_query.filter(Item.year == query_terms['year'])
    if query_terms.get('genre'):
        pass # TODO: query by genre!! join with media_genre?

    # for key in query_terms: # build query
    #     new_query = new_query.filter(Item.key == query_terms[key])

        # FIXME: how do I use the keys to point at the attributes I care about? apparently putting a variable in there doesn't work.
        # Also, note this does not add author or anything type-specific! need to join queries in that case.

    if query_terms.get('media_type') == 'book':
        new_query = new_query.join(Book)
        if query_terms.get('author'):
            new_query = new_query.filter(Book.author == query_terms['author'])
    elif query_terms.get('media_type') == 'movie':
        new_query = new_query.join(Movie)
        if query_terms.get('length'):
            new_query = new_query.filter(Movie.length == query_terms['length'])
    elif query_terms.get('media_type') == 'tv_ep':
        new_query = new_query.join(TVEpisode)
        if query_terms.get('season'):
            new_query = new_query.filter(TVEpisode.season == query_terms['season'])

    return new_query.all()


def create_genre(genre_name):
    """ Create and return a new genre. 
    e.g.
        >>> create_genre('Climate Fiction')
        <Genre genre_name=Climate Fiction>
    """

    check_genre = Genre.query.filter(Genre.genre_name==genre_name).first()

    if check_genre: # genre already exists!
        return check_genre
    else:
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


def remove_from_user_library(user, user_media_item=None, user_media_id=None):
    """ Remove the specified item from a user's library. """

    if user_media_item:
        user_media_id = user_media_item.user_media_id
    
    user_item = get_user_item_by_user_media_id(user.user_id, user_media_id)
    title = user_item.item.title

    db.session.delete(user_item) # delete the record in the user_media table with that user_media_id
    db.session.commit()
    # delete any records in the collections_media table with that user_media_id
    # later: delete any user_updates with that user_media_id

    print(f'{title} was successfully removed from your library!')


def get_user_item_by_user_media_id(user_id, user_media_id):
    """ Given the user_media_id, return the user's item. """

    return UserMedia.query.filter(UserMedia.user_media_id==user_media_id).first()


def get_item_by_user_media_id(user_id, user_media_id):
    """ Given the user_media_id, return the main db item. """

    return UserMedia.query.join(User).filter(User.user_id==user_id).join(Item).filter(UserMedia.user_media_id==user_media_id).first().item


def create_collection(user, collection_name):
    """ Create and return a new collection. """

    collection = Collection(user_id=user.user_id, name=collection_name)

    db.session.add(collection)
    db.session.commit()

    return collection


def delete_collection(user, collection_name):
    """ Delete the specified collection. """

    # TODO: WRITE THIS

    print(f'The collection was deleted. (except not actually yet... todo!)')


def get_user_media_id(user, media_item):
    """ Query database and return the user_media_id association between 
        a user_id and a media_item. """

    return UserMedia.query.filter(UserMedia.user_id==user.user_id, 
                    UserMedia.item_id==media_item.item_id).first().user_media_id


def assign_to_collection(user, media_item, collection):
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


#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    import doctest
    # import unittest
    from server import app
    connect_to_db(app, echo=False)
    # unittest.main()
    result = doctest.testmod() # (verbose=2)
    if not result.failed:
        print("ALL DOCTESTS PASSED. GOOD WORK!")
