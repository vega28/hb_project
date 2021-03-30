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
    profile_pic = db.Column(db.String(100)) # link to image

    # TODO: describe relationships here

    def __repr__(self):
        return f'<User fname={self.fname} lname={self.lname}>'


class Item(db.Model):
    """ A media item of any type. """

    __tablename__ = 'media'

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('media_types.type_id'), nullable=False) # foreign key to media_types table
    cover = db.Column(db.String(100)) # link to image
    description = db.Column(db.Text)

    media_type = db.relationship('Type', backref='items') # FIXME: technically want this to refer to Type.media_type... otherwise is it necessary since it's indistinct from type_id above?
    genres = db.relationship('Genre', secondary='media_genres', backref='items')

    def __repr__(self):
        return f'<Media Item title={self.title} media_type={self.media_type}>'


class Type(db.Model):
    """ A specific type of media. """

    __tablename__ = 'media_types'

    type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    media_type = db.Column(db.String(20), nullable=False)

    # items = a list of media items of the specified media_type

    def __repr__(self):
        return f'<Type media_type={self.media_type} type_id={self.type_id}>'



class Genre(db.Model):
    """ A specific genre of media. """

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_name = db.Column(db.String(30), unique=True, nullable=False)

    items = db.relationship('Item', secondary='media_genres', backref='genres') 

    def __repr__(self):
        return f'<Genre genre_name={self.genre_name}>'



class MediaGenre(db.Model):
    """ Association table between media and genres. """

    __tablename__ = 'media_genres'

    media_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('media.item_id'), nullable=False) # foreign key linking to media
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False) # foreign key linking to genres

    def __repr__(self):
        return f'<ClassName attribute={self.attribute}>'



# class Book(db.Model):
#     """ A book. """
#     __tablename__ = 'books'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



# class TVShow(db.Model):
#     """ A TV show. """
#     __tablename__ = 'tv_shows'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



# class Movie(db.Model):
#     """ A movie. """
#     __tablename__ = 'movies'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



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



# class Collection(db.Model):
#     """ A user-defined collection of media. """
#     __tablename__ = 'collections'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



# class CollectionMedia(db.Model):
#     """ Association table between Collections and UserMedia """
#     __tablename__ = 'collections_media'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



# class UserMedia(db.Model):
#     """ Media items specific to a user. """
#     __tablename__ = 'user_media'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'



# class UserLog(db.Model):
#     """ A log entry update by a user. """
#     __tablename__ = 'user_log'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'

# TODO: Times consumed as its own table or part of the above?!




# --- class definition structure --- # 

# class ClassName(db.Model):
#     """ <class description> """
#     __tablename__ = '<tablename>'
#     # add attributes here
#     # describe relationships here
#     def __repr__(self):
#         return f'<ClassName attribute={self.attribute}>'

