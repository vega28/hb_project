""" Models for Library App """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ A user of the app. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True) 
    pwd = db.Column(db.String(25), nullable=False) # keep it secret, keep it safe!
    profile_pic = db.Column(db.Text) # link to image

    # media = a list of media Item objects specific to this user's library 
    # updates = a list of this user's updates

    def __repr__(self):
        return f'<User fname={self.fname} lname={self.lname}>'


class Item(db.Model):
    """ A media item of any type. """

    __tablename__ = 'media'

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, 
                        db.ForeignKey('media_types.type_id'), 
                        nullable=False) # foreign key to media_types table
    cover = db.Column(db.Text) # link to image
    description = db.Column(db.Text)
    year = db.Column(db.Integer) # release year

    # updates = a list of UserUpdates about this media item
    media_type = db.relationship('Type', backref='items') # returns media_type object
    genres = db.relationship('Genre', 
                            secondary='media_genres', 
                            backref='items')
    # users = db.relationship('User', secondary='user_media', backref='items') # TODO: check these relationships...

    def __repr__(self):
        return f'<Media Item title={self.title}>'


class Type(db.Model):
    """ A specific type of media. """

    __tablename__ = 'media_types'

    type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    media_type = db.Column(db.String(20), nullable=False)
    # TODO: make name of media_type the primary key, change foreign key in Item class

    # items = a list of media Item objects of the specified media_type 

    def __repr__(self):
        return f'<Type media_type={self.media_type} type_id={self.type_id}>'



class Genre(db.Model):
    """ A specific genre of media. """

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_name = db.Column(db.String(30), unique=True, nullable=False)

    # items = a list of media items of the specified genre 

    def __repr__(self):
        return f'<Genre genre_name={self.genre_name}>'



class MediaGenre(db.Model):
    """ Association table between media and genres. """

    __tablename__ = 'media_genres'

    media_genre_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    item_id = db.Column(db.Integer, 
                        db.ForeignKey('media.item_id'), 
                        nullable=False) # foreign key linking to media
    genre_id = db.Column(db.Integer, 
                        db.ForeignKey('genres.genre_id'), 
                        nullable=False) # foreign key linking to genres

    def __repr__(self):
        return f'<MediaGenre media_genre_id={self.media_genre_id}>'



class Book(Item): 
    """ A book - subclassed from media Item. """

    __tablename__ = 'books'

    # add attributes here
    book_id = db.Column(db.Integer, 
                        db.ForeignKey('media.item_id'), 
                        primary_key=True)
    author = db.Column(db.String, nullable=False)
    edition = db.Column(db.String)
    pages = db.Column(db.Integer) # length in pages
    isbn = db.Column(db.Integer, unique=True) # check if there exists a specific format for ISBN in python?

    # describe relationships here # TODONE: do these inherit from the parent class as well? YES.

    def __repr__(self):
        return f'<Book title={self.title} author={self.author}>' 



class Movie(Item):
    """ A movie - subclassed from media Item. """

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer,
                        db.ForeignKey('media.item_id'),
                        primary_key=True)
    length = db.Column(db.Integer) # length of movie in minutes

    # describe relationships here

    def __repr__(self):
        return f'<Movie title={self.title} year={self.year}>'



class TVEpisode(Item):
    """ An episode of a TV show - subclassed from media Item. """

    __tablename__ = 'tv'

    ep_id = db.Column(db.Integer,
                      db.ForeignKey('media.item_id'),
                      primary_key=True)
    show_title = db.Column(db.String, nullable=False)
    ep_length = db.Column(db.Integer) # length of episode in minutes
    season = db.Column(db.Integer) # which season is the episode in?
    ep_of_season = db.Column(db.Integer) # which episode of that season?

    # describe relationships here

    def __repr__(self):
        return f'<TVEpisode show_title={self.show_title} title={self.title}>'



# class Comic(db.Model): # NTH
#     """ A comic book. """
#     __tablename__ = 'comics'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



# class Podcast(db.Model): # NTH
#     """ A podcast. """
#     __tablename__ = 'podcasts'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



# class Game(db.Model): # NTH
#     """ A game. """
#     __tablename__ = 'games'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



class Collection(db.Model):
    """ A user-defined collection of media. """

    __tablename__ = 'collections'

    collection_id = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=False) # foreign key linking to users
    name = db.Column(db.String(30), nullable=False)

    # user_media = a list of UserMedia objects that are in this collection

    def __repr__(self):
        return f'<Collection name={self.name} user_id={self.user_id}>'



class CollectionUserMedia(db.Model):
    """ Association table between Collections and UserMedia """

    __tablename__ = 'collections_user_media'

    collections_user_media_id = db.Column(db.Integer, 
                                        autoincrement=True, 
                                        primary_key=True)
    collection_id = db.Column(db.Integer, 
                              db.ForeignKey('collections.collection_id'), 
                              nullable=False) # foreign key linking to collections
    user_media_id = db.Column(db.Integer, 
                              db.ForeignKey('user_media.user_media_id'), 
                              nullable=False) # foreign key linking to user_media

    def __repr__(self):
        return f'<CollectionUserMedia collections_user_media_id={self.collections_user_media_id}>'



class UserMedia(db.Model):
    """ Middle table: media items specific to a user. """

    __tablename__ = 'user_media'

    user_media_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=False) # foreign key linking to users
    item_id = db.Column(db.Integer, 
                        db.ForeignKey('media.item_id'), 
                        nullable=False) # foreign key linking to media
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False) # check this - how to make it NOW?
    source = db.Column(db.String(30))

    user = db.relationship('User', backref='media')
    item = db.relationship('Item', backref='user_media')
    collections = db.relationship('Collection', 
                                secondary='collections_user_media', 
                                backref='user_media')

    def __repr__(self):
        return f'<UserMedia user_media_id={self.user_media_id}>'



class UserUpdate(db.Model):
    """ Middle table: an update logged by a user. """

    __tablename__ = 'user_updates'

    update_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=False) # foreign key linking to users
    item_id = db.Column(db.Integer, 
                        db.ForeignKey('media.item_id'), 
                        nullable=False) # foreign key linking to media
    update_entered_at = db.Column(db.DateTime, nullable=False) # check this - how to make it NOW?
    date = db.Column(db.DateTime) # consider format - day/mo/yr needed?
    start_bool = db.Column(db.Boolean, nullable=False)
    end_bool = db.Column(db.Boolean, nullable=False)
    dnf = db.Column(db.Boolean)
    num_times_through = db.Column(db.Integer) # have this calculated based on previous records
    update_value = db.Column(db.Integer) # number of pages read or episode watched, etc.

    user = db.relationship('User', backref='updates')
    item = db.relationship('Item', backref='updates')

    def __repr__(self):
        return f'<UserUpdate update_id={self.update_id}>'










def connect_to_db(flask_app, db_uri='postgresql:///library', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    from server import app

    connect_to_db(app)