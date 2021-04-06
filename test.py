""" Script to test flask session and routes. """

from unittest import TestCase
from server import app
from flask import session
import crud
import model
import os


def example_data():
    """ Create some sample data. """

    # In case this is run more than once, empty out existing data
    model.User.query.delete()
    model.Item.query.delete()

    # Add media types
    t1 = model.Type(media_type='book')
    t2 = model.Type(media_type='movie')
    t3 = model.Type(media_type='tv')

    model.db.session.add_all([t1, t2, t3])
    model.db.session.commit()

    # Add sample users and media
    rose = model.User(fname='Rose', lname='Tyler', email='rose@tardis.com', pwd='doctorwho', profile_pic='https://bit.ly/3fPVcfn')
    bob = model.User(fname='Bob', lname='Bobson', email='bob@bob.com', pwd='bob', profile_pic='https://images.gr-assets.com/authors/1406058780p8/3089156.jpg')

    cosmos = model.Item(title='Cosmos', type_id=1,
                            cover='http://books.google.com/books/content?id=cDKODQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                            description="Presents an illustrated guide to the universe and to Earth's relationship to it, moving from theories of creation to humankind's discovery of the cosmos, to general relativity, to space missions, and beyond.")
    contact = model.Book(title='Contact', type_id=1, 
                            cover='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1567132653l/94786._SY475_.jpg',
                            description="In December, 1999, a multinational team journeys out to the stars, to the most awesome encounter in human history. Who -- or what -- is out there? \nIn Cosmos, Carl Sagan explained the universe. In Contact, he predicts its future -- and our own.",
                            author='Carl Sagan', 
                            pages=434)
    mononoke = model.Movie(title='Princess Mononoke', type_id=2, 
                            cover='https://m.media-amazon.com/images/M/MV5BNGIzY2IzODQtNThmMi00ZDE4LWI5YzAtNzNlZTM1ZjYyYjUyXkEyXkFqcGdeQXVyODEzNjM5OTQ@._V1_UX182_CR0,0,182,268_AL_.jpg', 
                            description="On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony. In this quest he also meets San, the Mononoke Hime.", 
                            length=134, 
                            year=1997)
    sg1_ep1 = model.TVEpisode(title='Children of the Gods', type_id=3, 
                            cover='https://m.media-amazon.com/images/M/MV5BMTc3MjEwMTc5N15BMl5BanBnXkFtZTcwNzQ2NjQ4NA@@._V1_UX182_CR0,0,182,268_AL_.jpg',
                            description="Colonel Jack O'Neill is brought out of retirement to lead a new expedition back to Abydos, only to find an old friend, a new enemy and a far wider use of the Stargate.",
                            show_title='Stargate SG-1', 
                            ep_length=92, 
                            season=1)

    model.db.session.add_all([bob, rose, cosmos, contact, mononoke, sg1_ep1])
    model.db.session.commit()



class FlaskTestsDatabase(TestCase):
    """ Flask tests that use the database. """

    def setUp(self):
        """ Stuff to do before EVERY test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        model.connect_to_db(app, 'postgresql:///testdb', echo=False)

        model.db.create_all()
        example_data()

    def tearDown(self):
        """ Stuff to do at end of EVERY test. """

        model.db.session.remove()
        model.db.drop_all()
        model.db.engine.dispose()

    def test_user_list(self):
        """ Test user list page. """

        result = self.client.get('/users')
        self.assertIn(b'rose@tardis.com', result.data)

    def test_user_details(self):
        """ Test user details page. """

        result = self.client.get('/users/2')
        self.assertIn(b'Tyler', result.data)

    def test_media_list(self):
        """ Test media list page. """

        result = self.client.get('/media')
        self.assertIn(b'Princess Mononoke', result.data)

    def test_media_details(self):
        """ Test media details page. """

        result = self.client.get('/media/1')
        self.assertIn(b'Cosmos', result.data)




#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')

    unittest.main(verbosity=2)