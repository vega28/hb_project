""" Things to (for now...) copy-paste into interactive mode for testing model.py """

db.create_all()

bob = User(fname='bob', lname='bob', email='bob@bob.com', pwd='bob')
db.session.add(bob)
db.session.commit()

User.query.filter(User.fname == 'bob').update({'lname':'bobson'})
db.session.commit()

new_type = Type(media_type='book')
db.session.add(new_type)
db.session.commit()

cosmos = Item(title='cosmos', type_id = 1)
db.session.add(cosmos)
db.session.commit()

new_genre = Genre(genre_name = 'science')
db.session.add(new_genre)
db.session.commit()

cosmos_genre = MediaGenre(item_id=cosmos.item_id, genre_id=new_genre.genre_id)
db.session.add(cosmos_genre)
db.session.commit()

bob_cosmos = UserMedia(user_id=bob.user_id, item_id=cosmos.item_id, rating=5)
db.session.add(bob_cosmos)
db.session.commit()