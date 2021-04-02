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

    # all_media = crud.get_all_media() # FIXME KeyError: 'SQLALCHEMY_TRACK_MODIFICATIONS'

    return render_template('media.html') # , all_media=all_media)


@app.route('/users')
def list_users():
    """ View list of all users. """

    all_users = crud.get_all_users() # FIXME: KeyError: 'SQLALCHEMY_TRACK_MODIFICATIONS'

    return render_template('users.html', all_users=all_users)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')