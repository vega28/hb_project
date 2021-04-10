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
def search_db_for_media_item():
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

    db_matches = crud.search_db(query_terms=query_terms)
    db_matches_dict = {}
    for item in db_matches:
        db_matches_dict[item.item_id] = {'title': item.title, 'cover': item.cover}

    return db_matches_dict


@app.route('/review_media')
def review_media_item():
    """ Ask for user's review and rating of new media item. """

    if session.get('item_to_add'):
        del session['item_to_add']
    item = crud.get_item_by_id(request.args.get('chosen-item'))

    session['item_to_add'] = {'title': item.title, 'item_id': item.item_id, 'cover': item.cover}

    # TODO: check if item already associated with user's media!

    return render_template('review_media.html')


@app.route('/review_new_media')
def review_new_media_item():
    """ Ask for user's review and rating of new media item. 
        Add new item to database. """

    if session.get('item_to_add'):
        del session['item_to_add']
    
    # create new item with the appropriate media_type. add to db.
    if session['search_query']['media_type'] == 'book':

        list_num = request.args.get('list_num')
        author = request.args.get(list_num+'-authors')
        if author:
            author = author[0]
        item_data = {'id': request.args.get(list_num+'-id'),
                    'title': request.args.get(list_num+'-title'),
                    'author': author,
                    'cover': request.args.get(list_num+'-cover'),
                    'description': request.args.get(list_num+'-description'),
                    'pages': request.args.get(list_num+'-pageCount')}

        item = crud.create_book(title=item_data['title'], 
                                type_id=1, # FIXME: currently hardcoded 
                                author=item_data.get('author'), 
                                cover=item_data.get('cover'), 
                                description=item_data.get('description'), 
                                # year=item_data.get('publishedDate'), # TODO: fix format 
                                # edition=None, 
                                pages=item_data.get('pages')) 
                                # isbn=None)

        # return render_template('search_results.html', list_num=list_num, item_data=item_data) ### temp debugging route - will go to review page when item is added to db correctly!


    # elif session['search_query']['media_type'] == 'movie':
    #     item = crud.create_movie(title, type_id, cover=None, description=None, length=None, 
    #             year=None)# TODO
    # elif session['search_query']['media_type'] == 'tv_ep':
    #     item = crud.create_tv_ep(title, type_id, show_title, cover=None, description=None, 
    #             year=None, ep_length=None, season=None, ep_of_season=None)# TODO
    # else:
    #     item = crud.create_item(title, type_id, cover=None, description=None, year=None) # TODO

    # retrieve user's rating, review, and source. route to /add_media

    session['item_to_add'] = {'title': item.title, 'item_id': item.item_id, 'cover': item.cover}

    return render_template('review_media.html')


@app.route('/add_media')
def add_media_item():
    """ Add item to user's media. """

    crud.store_media_in_user_library(user=crud.get_user_by_id(session['user_id']), 
            media_item=crud.get_item_by_id(session['item_to_add']['item_id']), 
            rating=request.args.get('rating'), 
            review=request.args.get('review'), 
            source=request.args.get('source'))

    flash(f"{session['item_to_add']['title']} has been added to your library.")

    return redirect('/')


@app.route('/api_search')
def search_api_for_media_item():
    """ Make GET request to the appropriate API. 
        Add item to the database. """

    if session['search_query']['media_type'] == 'book':
        # Google Books API
        uri = 'https://www.googleapis.com/books/v1/volumes'
        payload = {'access_token': GOOGLE_BOOKS_TOKEN,
                    'maxResults': 20,
                    'q': f"{session['search_query']['title']} {session['search_query']['author']}"}
        res = requests.get(uri, params=payload)
        data = res.json() # type dict

        return render_template('api_search_results.html', pformat=pformat, data=data)

    elif session['search_query']['media_type'] == 'movie':
        pass # IMDB movie API
        # TODO: allow user to select an option to add to db - get its tag, do another request to get that volume's info, and add to db

    elif session['search_query']['media_type'] == 'tv_ep':
        pass # IMDB TV API
        # TODO: allow user to select an option to add to db - get its tag, do another request to get that volume's info, and add to db

    else:
        pass # user creates their own new type and item


@app.route('/manage_media')
def manage_media():
    """ Show media management page to user. 
        Collections functionality: 
            create, delete, add items to, remove items from, rename
        Media item functionality:
            delete, add to collection, edit rating/review/source
    """
    user = crud.get_user_by_id(session['user_id'])
    return render_template('manage_media.html', user=user)


@app.route('/manage_item', methods=['POST'])
def manage_item():
    """ Allow user to manage their media items. 
        functionality:
            delete item 
            add item to collection - assign_to_collection(user, media_item, collection)
            edit rating/review/source
            NTH: see/edit updates associated with this item.
    """
    user_media_id = request.form.get('user_media_id') 
    user = crud.get_user_by_id(session['user_id'])
    item = crud.get_item_by_user_media_id(user.user_id, user_media_id) 

    return render_template('manage_item.html', user=user, item=item)


@app.route('/manage_collection')
def manage_collection():
    """ Allow user to manage their collections. 
        Functionality: 
            create collection - create_collection(user, collection_name)
            delete collection - delete_collection(user, collection_name)
            remove items from collection
            rename collection
            NTH: bulk add items to collection
            NTH: arrange items in collection
    """
    # TODO: get collection_id back from manage.js and create management functions
    user = crud.get_user_by_id(session['user_id'])
    collection = crud.get_collection_by_id(collection_id)
    return render_template('manage_collection.html', user=user, collection=collection)



#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')