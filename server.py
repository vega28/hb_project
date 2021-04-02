""" Server for library app. """

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """ Show the homepage. """

    return render_template('homepage.html')


@app.route('/media')
def list_media():
    """ View list of all media. """

    all_media = crud.get_all_media() 

    return render_template('media.html', all_media=all_media)


@app.route('/media/<item_id>')
def media_item_details(item_id):
    """ Show details for the specified media item. """

    item = crud.get_item_by_id(item_id)

    return render_template('item_details.html', item=item)


@app.route('/users')
def list_users():
    """ View list of all users. """

    all_users = crud.get_all_users() 

    return render_template('users.html', all_users=all_users)


@app.route('/users/<user_id>')
def user_details(user_id):
    """ Show details for the specified user. """

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


# log in route


# sign up route


@app.route('/user_homepage') # make this user-specific...
def show_user_homepage():
    """ Show a logged-in user their personal homepage. """

    # TODO: write me!
    # user = get user!

    # return render_template('user_homepage.html', user=user)


# also want user-specific media page, add media page, collections page


# browse all media route (by genre, media type, etc.)






if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')