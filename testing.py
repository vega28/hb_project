""" Things to (for now...) copy-paste into interactive mode for testing model.py """

db.create_all()

# ADD USER
bob = User(fname='bob', lname='bob', email='bob@bob.com', pwd='bob')
db.session.add(bob)
db.session.commit()

User.query.filter(User.fname == 'bob').update({'lname':'bobson'})
db.session.commit()

# CHECK MEDIA TYPES
booktype = Type(media_type='book')
db.session.add(booktype)
db.session.commit()

movietype = Type(media_type='movie')
db.session.add(movietype)
db.session.commit()

tvtype = Type(media_type='tv')
db.session.add(tvtype)
db.session.commit()

# CHECK ITEMS
cosmos = Item(title='Cosmos', type_id = 1)
db.session.add(cosmos)
db.session.commit()

contact = Book(title='Contact',type_id=booktype.type_id,author='Carl Sagan')
db.session.add(contact)
db.session.commit()

sunshine = Movie(title='Sunshine',type_id=movietype.type_id,length=107,year=2007)
db.session.add(sunshine)
db.session.commit()

sg1_ep1 = TVEpisode(title='Children of the Gods', type_id=tvtype.type_id, show_title='Stargate SG-1', length=92, season=1)
db.session.add(sg1_ep1)
db.session.commit()

# CHECK GENRES
genre1 = Genre(genre_name = 'Science')
db.session.add(genre1)
db.session.commit()

genre2 = Genre(genre_name = 'Science Fiction')
db.session.add(genre2)
db.session.commit()

cosmos_genre = MediaGenre(item_id=cosmos.item_id, genre_id=genre1.genre_id)
db.session.add(cosmos_genre)
db.session.commit()

contact_genre = MediaGenre(item_id=contact.item_id, genre_id=genre2.genre_id)
db.session.add(contact_genre)
db.session.commit()

sunshine_genre = MediaGenre(item_id=sunshine.item_id, genre_id=genre2.genre_id)
db.session.add(sunshine_genre)
db.session.commit()

sg1_genre = MediaGenre(item_id=sg1_ep1.item_id, genre_id=genre2.genre_id)
db.session.add(sg1_genre)
db.session.commit()

# ADD USER-SPECIFIC MEDIA
bob_cosmos = UserMedia(user_id=bob.user_id, item_id=cosmos.item_id, rating=5)
db.session.add(bob_cosmos)
db.session.commit()

bob_sunshine = UserMedia(user_id=bob.user_id, item_id=sunshine.item_id, rating=5)
db.session.add(bob_sunshine)
db.session.commit()

bob_sg1 = UserMedia(user_id=bob.user_id, item_id=sg1_ep1.item_id, rating=4)
db.session.add(bob_sg1)
db.session.commit()

# CHECK COLLECTIONS
favorites = Collection(user_id=bob.user_id, name='Favorites')
db.session.add(favorites)
db.session.commit()

fave_book = CollectionUserMedia(collection_id=favorites.collection_id, user_media_id=bob_cosmos.user_media_id)
db.session.add(fave_book)
db.session.commit()

fave_movie = CollectionUserMedia(collection_id=favorites.collection_id, user_media_id=bob_sunshine.user_media_id)
db.session.add(fave_movie)
db.session.commit()

fave_tv = CollectionUserMedia(collection_id=favorites.collection_id, user_media_id=bob_sg1.user_media_id)
db.session.add(fave_tv)
db.session.commit()
