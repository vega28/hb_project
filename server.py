""" Server for library app. """

from flask import (Flask, render_template, request, flash, session, redirect)
import os
from jinja2 import StrictUndefined
from pprint import pformat
import requests

from model import connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

GOOGLE_BOOKS_TOKEN = os.environ['GOOGLE_BOOKS_TOKEN']
IMDB_API_KEY = os.environ['IMDB_API_KEY']

@app.route('/')
def show_homepage():
    """ Show the homepage. 
        NOTE: If user is logged in, show the user-specific homepage. """

    logged_in = session.get('user_id',None)

    if logged_in:
        user = crud.get_user_by_id(session['user_id'])
        return render_template('user_homepage.html', user=user)
    else:
        return render_template('homepage.html')



# browse all media route (by genre, media type, etc.) TODO: organize by JS?
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


@app.route('/log_in')
def show_login_page():
    """ Show the log-in page for an existing user. """
    if session.get('user_id',None):
        flash(f'You are already logged in!')
        return redirect('/')
    else:
        return render_template('log_in.html')


@app.route('/verify_login', methods=['POST'])
def verify_login():
    """ Verify a user's login information. """

    email = request.form.get('email')
    pwd = request.form.get('pwd')

    user = crud.get_user_by_email(email)

    if user and user.pwd == pwd:
        flash(f'Welcome back, {user.fname}! You are now logged in.')
        session['user_id'] = user.user_id
    else:
        flash(f'User email and/or password is incorrect. Please try again.')

    return redirect('/')


@app.route('/log_out')
def log_out():
    """ Log user out of session. """

    del session['user_id']
    flash('You have been logged out.')

    return redirect('/')


@app.route('/sign_up')
def show_sign_up_page():
    """ Show the sign-up page for a new user. """

    return render_template('create_account.html')


@app.route('/new_user', methods=['POST'])
def register_user():
    """ Create a new user. 
        Verify that the email is unique and the passwords match. """

    fname = request.form.get('fname')    
    lname = request.form.get('lname')
    email = request.form.get('email') # TODO: verify that this is an email format
    pwd = request.form.get('pwd')
    pwd2 = request.form.get('pwd_confirm')
    profile_pic = request.form.get('profile_pic')

    if crud.get_user_by_email(email):
        flash('That email is taken. Please try a different email.')
    elif pwd == pwd2:
        user = crud.create_user(fname, lname, email, pwd, profile_pic)
        session['user_id'] = user.user_id
        flash(f'Welcome, {fname}! Your account has been created. You are now logged in.')
    else:
        flash('Your passwords do not match. Please try again.')

    return redirect('/')


# add media item (check if in db first, then make get request to appropriate API)
@app.route('/search')
def search_for_media_item():
    """ Show search page. """

    # session['media_types'] = crud.get_all_types() # use this if you get the jinja template together for searchpage.html
    genres = crud.get_all_genres()

    return render_template('searchpage.html', genres=genres)


@app.route('/process_search')
def process_search():
    """ Search database for the specified media item.
        Show ALL results matching any ONE keyword. 
        Let user select the correct item, if it exists.
        If not in the database, redirect to /add_media route. """

    if session.get('search_query'):
        del session['search_query']
    media_type = request.args.get('media_type')
    session['search_query'] = {'media_type': media_type,
                                'title': request.args.get('title'),
                                'year': request.args.get('year'),
                                'main_genre': request.args.get('genre')}
    if media_type == 'book':
        session['search_query']['author'] = request.args.get('author')
    elif media_type == 'movie':
        session['search_query']['length'] = request.args.get('length')
    elif media_type == 'tv_ep':
        session['search_query']['season'] = request.args.get('season')

    query_terms = {}
    for term in session['search_query']:
        if session['search_query'][term]:
            query_terms[term] = session['search_query'][term]
    print('********************************************')
    print(query_terms)

    db_matches = crud.search_db(query_terms=query_terms)
    db_matches_dict = {}
    for item in db_matches:
        db_matches_dict[item.item_id] = {'title': item.title, 'cover': item.cover}

    

    return db_matches_dict
    # return render_template('search_results.html', db_title_matches=db_title_matches)


@app.route('/add_media')
def add_media_item():
    """ Make GET request to the appropriate API.
        Add item to the database. """

    if session['search_query']['media_type'] == 'book':
        # Google Books API
        uri = 'https://www.googleapis.com/books/v1/volumes'
        payload = {'access_token': GOOGLE_BOOKS_TOKEN,
                    'maxResults': 20,
                    'q': f"{session['search_query']['title']} {session['search_query']['author']}"}
        res = requests.get(uri, params=payload)
        data = res.json()
        return render_template('api_search_results.html', pformat=pformat, data=data)
        # TODO: allow user to select an option to add to db 
        #       get tag for selected item
        #       do another request to get that volume's info
        #       add to db

    elif session['search_query']['media_type'] == 'movie':
        pass # IMDB movie API
        # TODO: allow user to select an option to add to db - get its tag, do another request to get that volume's info, and add to db

    elif session['search_query']['media_type'] == 'tv_ep':
        pass # IMDB TV API
        # TODO: allow user to select an option to add to db - get its tag, do another request to get that volume's info, and add to db

    else:
        pass # user creates their own new type and item




#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')