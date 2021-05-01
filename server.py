""" Server for library app. """

from flask import (Flask, render_template, request, flash, session, redirect)
import os
from jinja2 import StrictUndefined
from pprint import pformat
import requests
from bokeh.plotting import figure
from bokeh.embed import components
from math import pi
from bokeh.palettes import Category20
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
import pandas as pd
from random import randint
import json
from datetime import datetime, date, time

from model import connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

GOOGLE_BOOKS_TOKEN = os.environ['GOOGLE_BOOKS_TOKEN']
IMDB_API_KEY = os.environ['IMDB_API_KEY']


#----------------------------------------------------------------------#
# *** Homepages                                                        #
#----------------------------------------------------------------------#

@app.route('/')
def show_homepage():
    """ Show the homepage. 
        NOTE: If user is logged in, show the user-specific homepage. """

    logged_in = session.get('user_id',None)

    if logged_in:
        user = crud.get_user_by_id(session['user_id'])
        return render_template('user_homepage_v2.html', user=user)
    else:
        return render_template('homepage.html')


#----------------------------------------------------------------------#
# *** Routes Visible Without Logging In                                #
#----------------------------------------------------------------------#

# browse all media route (by genre, media type, etc.) # TODO: filter with JS?
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


#----------------------------------------------------------------------#
# *** Routes Related to User Login Status                              #
#----------------------------------------------------------------------#

@app.route('/log_in')
def show_login_page():
    """ Show the log-in page for an existing user. """

    if session.get('user_id', None):
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
        session['user_name'] = user.fname
    else:
        flash(f'User email and/or password is incorrect. Please try again.')

    return redirect('/')


@app.route('/log_out')
def log_out():
    """ Log user out of session. """

    del session['user_id']
    del session['user_name']
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
        if profile_pic == '':
            profile_pic = '/static/images/default_pf2.png'
        user = crud.create_user(fname, lname, email, pwd, profile_pic)
        session['user_id'] = user.user_id
        flash(f'Welcome, {fname}! Your account has been created. You are now logged in.')
    else:
        flash('Your passwords do not match. Please try again.')

    return redirect('/')


#----------------------------------------------------------------------#
# *** Routes Related to Media Search                                   #
#----------------------------------------------------------------------#

# add media item (check if in db first, then make get request to appropriate API)
@app.route('/search')
def search_db_for_media_item():
    """ Show search page. """

    # session['media_types'] = crud.get_all_types() # TODO: use this if you get the jinja template together for searchpage.html
    genres = crud.get_all_genres()

    return render_template('searchpage.html', genres=genres)


@app.route('/process_search')
def process_search():
    """ Search database for the specified media item.
        Show results matching ALL keywords.
        Let user select the correct item, if it exists.
        If not in the database, redirect to /add_media route. """

    if session.get('search_query'): # if previously had other search terms
        del session['search_query'] # clear all fields

    media_type = request.args.get('media_type')
    session['search_query'] = {'media_type': media_type,
                                'title': request.args.get('title'),
                                'year': request.args.get('year'),
                                'genre': request.args.get('genre')}
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
        db_matches_dict[item.item_id] = {'title': item.title, 
                                        'cover': item.cover}

    return db_matches_dict


@app.route('/api_search')
def search_api_for_media_item():
    """ Make GET request to the appropriate API. 
        Display the results from the API response to allow user to choose one. """

    if session['search_query']['media_type'] == 'book':
        # Google Books API
        uri = 'https://www.googleapis.com/books/v1/volumes'
        payload = {'access_token': GOOGLE_BOOKS_TOKEN,
            'maxResults': 20,
            'q': f"{session['search_query']['title']} {session['search_query']['genre']} {session['search_query']['year']} {session['search_query']['author']}"}
        res = requests.get(uri, params=payload)
        data = res.json() # type dict

        return render_template('api_search_results.html', 
                                pformat=pformat, data=data)

    # elif session['search_query']['media_type'] == 'movie':
    #     pass # IMDB movie API
    #     # TODO: allow user to select an option to add to db - get its tag, do another request to get that volume's info, and add to db
    #     uri = 'https://imdb-api.com/en/API/SearchMovie/'
    #     payload = {'apiKey': IMDB_API_KEY,
    #         'expression': f"{session['search_query']['title']} {session['search_query']['year']}"} # {session['search_query']['length']}  {session['search_query']['genre']}
    #     res = requests.get(uri, params=payload)
    #     data = res.json()

    #     return render_template('api_search_results.html', 
    #                             pformat=pformat, data=data) # TODO: check this... not same as books!!

    #// elif session['search_query']['media_type'] == 'tv_ep':
    #//     pass # IMDB TV API
    
    #// else:
    #//     pass # user creates their own new type and item


@app.route('/review_new_media')
def review_new_media_item():
    """ Parse information about new item.
        Create and add new item to database. """

    if session.get('item_to_add'): # if previously added a new item
        del session['item_to_add'] # then clear all fields 
    
    # TODO: check if item already in db! ask if user is sure they want a 2nd instance

    # create new item with the appropriate media_type. 
    if session['search_query']['media_type'] == 'book':

        # parse item information from html form:
        list_num = request.args.get('list_num')
        author = request.args.get(list_num+'-authors')
        if author:
            author = author[0]
        item_data = {'id': request.args.get(list_num+'-id'),
                    'title': request.args.get(list_num+'-title'),
                    'author': author,
                    'cover': request.args.get(list_num+'-cover'),
                    'description': request.args.get(list_num+'-description'),
                    'pages': request.args.get(list_num+'-pageCount'),
                    'genres': request.args.get(list_num+'-genres')}

        # add new item to db:
        item = crud.create_book(title=item_data['title'], 
                                type_id=1, # FIXME: currently hardcoded 
                                author=item_data.get('author'), 
                                cover=item_data.get('cover'), 
                                description=item_data.get('description'), 
                                # year=item_data.get('publishedDate'), # TODO: fix format 
                                # edition=None, 
                                pages=item_data.get('pages')) 
                                # isbn=None)

        # assign genres:
        if item_data.get('genres'):
            genres = (item_data['genres']).strip("'][").split(', ')
            for genre in genres:
                new_genre = crud.create_genre(genre.title())
                crud.assign_genre(item, new_genre)

    # TODO: movie search!
    # elif session['search_query']['media_type'] == 'movie':
    #     item = crud.create_movie(title, type_id, cover=None, description=None, length=None, 
    #             year=None)
    #// elif session['search_query']['media_type'] == 'tv_ep':
    #//     item = crud.create_tv_ep(title, type_id, show_title, cover=None, description=None, 
    #//             year=None, ep_length=None, season=None, ep_of_season=None)# TODO
    #// else:
    #//     item = crud.create_item(title, type_id, cover=None, description=None, year=None) # TODO

    # add new item to session then go to review_media page:
    session['item_to_add'] = {'title': item.title, 
                            'item_id': item.item_id, 
                            'cover': item.cover}

    return render_template('review_media.html')


@app.route('/review_media')
def review_media_item():
    """ Ask for user's review and rating of new media item. """

    print('***********************DEBUG**********',request.args.get('chosen-item'))

    if session.get('item_to_add'):
        del session['item_to_add'] # clear all fields
    item = crud.get_item_by_id(request.args.get('chosen-item'))

    session['item_to_add'] = {'title': item.title, 
                            'item_id': item.item_id, 
                            'cover': item.cover}

    # TODO: check if item already associated with user's media!

    return render_template('review_media.html')


@app.route('/add_media')
def add_media_item():
    """ Add item to user's media. """

    start_date = request.args.get('start_date') if request.args.get('start_date') else None
    end_date = request.args.get('end_date') if request.args.get('end_date') else None
    dnf = True if request.args.get('dnf') else False
    crud.store_media_in_user_library(user=crud.get_user_by_id(session['user_id']), 
            media_item=crud.get_item_by_id(session['item_to_add']['item_id']), 
            rating=request.args.get('rating'), 
            review=request.args.get('review'), 
            source=request.args.get('source'),
            start_date=start_date,
            end_date=end_date,
            dnf=dnf)

    flash(f"{session['item_to_add']['title']} has been added to your library.")

    return redirect('/')


@app.route('/create_new_item')
def create_new_item():
    """ Show form to allow user to create a new item that is not in the 
        db and cannot be found by searching Google Books. """

    genres = crud.get_all_genres()

    return render_template('create_new_item.html', genres=genres,
                            sources=['library', 'owned', 'amazon', 'netflix', 'other'])


@app.route('/save_new_item', methods=['POST'])
def save_new_item():
    """ Save the user's new item to the database. 
        Redirect to the review page. """

    if request.form.get('media_type') == '':
        type_id = 7
    else:
        type_id = int(request.form.get('media_type'))

    item = crud.create_item(title=request.form.get('title'), 
                            type_id=type_id,
                            cover=request.form.get('cover'),
                            description=request.form.get('description'),
                            year=request.form.get('year') if request.form.get('year') else None,
                            note=request.form.get('note'))
    genre = crud.create_genre(request.form.get('genre'))
    crud.assign_genre(item, genre=genre)

    if session.get('item_to_add'):
        del session['item_to_add'] # clear all fields

    session['item_to_add'] = {'title': item.title, 
                            'item_id': item.item_id, 
                            'cover': item.cover}

    return render_template('review_media.html')


#----------------------------------------------------------------------#
# *** Routes Related to User's Media Management                        #
#----------------------------------------------------------------------#

@app.route('/view_item', methods=['POST'])
def view_item():
    """ Allow user to view details for a specified item in their library. """

    if session.get('item_to_edit'):
        del session['item_to_edit'] # clear all fields
    user_media_id = request.form.get('user_media_id') 
    user = crud.get_user_by_id(session['user_id'])
    user_item = crud.get_user_item_by_user_media_id(user.user_id, user_media_id) 
    session['item_to_edit'] = {'title': user_item.item.title, 
                        'item_id': user_item.item.item_id, 
                        'user_media_id': user_item.user_media_id,
                        'cover': user_item.item.cover,
                        'rating': user_item.rating,
                        'review': user_item.review,
                        'source': user_item.source,
                        'start_date': user_item.start_date,
                        'end_date': user_item.end_date,
                        'dnf': user_item.dnf}

    return render_template('view_item.html', user=user, 
                            user_item=user_item, db_item=user_item.item)


@app.route('/edit_item')
def edit_item_details():
    """ Show the current details for an item.
        Allow the user to edit the rating, review, and source. """

    user_item = crud.get_user_item_by_user_media_id(session['user_id'], 
                        session['item_to_edit']['user_media_id'])

    return render_template('edit_media_review.html', user_item=user_item,
                            sources=['library', 'owned', 'amazon', 'netflix', 'other'])


@app.route('/process_edits')
def process_item_details_edits():
    """ Process the edits provided by the user. """

    # update record in user_media table in db
    user_item = crud.get_user_item_by_user_media_id(session['user_id'], 
                        session['item_to_edit']['user_media_id'])
    start_date = request.args.get('start_date') if request.args.get('start_date') else None
    end_date = request.args.get('end_date') if request.args.get('end_date') else None
    crud.update_media_in_user_library(user=crud.get_user_by_id(session['user_id']), 
        media_item=user_item, 
        rating=request.args.get('rating'), 
        review=request.args.get('review'), 
        source=request.args.get('source'),
        start_date=start_date,
        end_date=end_date,
        dnf=request.args.get('dnf'))
    print(f"""**********dnf'{request.args.get("dnf")}'""")

    flash(f"Your details for {session['item_to_edit']['title']} have been edited.")

    return redirect('/')


@app.route('/delete_item', methods=['POST'])
def delete_item():
    """ Remove the specified item from the user's library. 
        NOTE this already removes it from the user's collections as well. """

    user = crud.get_user_by_id(session['user_id'])
    user_item = crud.get_user_item_by_user_media_id(user.user_id, 
                                        request.form.get('user_media_id')) 
    title = user_item.item.title
    crud.remove_from_user_library(user, user_media_item=user_item)

    return f'{title} has been removed from your library.'


@app.route('/choose_collection', methods=['POST'])
def choose_collection():
    """ Allow user to choose which collection to add their item to. """

    user = crud.get_user_by_id(session['user_id'])

    return render_template('choose_collection.html', user=user)


@app.route('/add_item_to_collection', methods=['POST'])
def add_item_to_collection():
    """ Add the specified item to the user's specified collection. """

    collection_id = request.form.get('collection_id') 
    user_item_id = request.form.get('user_item_id')
    user = crud.get_user_by_id(session['user_id'])
    user_item = crud.get_user_item_by_user_media_id(user.user_id, user_item_id)
    collection = crud.get_collection_by_id(collection_id)
    crud.assign_to_collection(user, user_item, collection)

    response = {'alert': f'{user_item.item.title} was successfully added to {collection.name}.',
                'cover': user_item.item.cover}

    return response


#----------------------------------------------------------------------#
# *** Routes Related to User's Collection Management                   #
#----------------------------------------------------------------------#

@app.route('/view_collection', methods=['POST'])
def view_collection():
    """ Allow user to view the specified collection. """

    collection_id = request.form.get('collection_id') 
    user = crud.get_user_by_id(session['user_id'])
    collection = crud.get_collection_by_id(collection_id)

    return render_template('view_collection.html', 
                            user=user, collection=collection)


@app.route('/list_collections')
def list_collections():
    """ Provide a list of a user's collections. """

    user_collections = {}
    user = crud.get_user_by_id(session['user_id'])
    for collection in user.collections:
        user_collections[collection.collection_id] = {'name': collection.name}

    return user_collections


@app.route('/create_collection', methods=['POST'])
def create_collection():
    """ Allow user to define a new collection """

    public = True if request.form.get('public') else False # JS was handing 'true' and 'false' strings, so this is my workaround for now!
    user = crud.get_user_by_id(session['user_id'])
    collection = crud.create_collection(user, 
                                        request.form.get('collection_name'), 
                                        public=public)

    return {'alert': f'{collection.name} has been added to your library.',
            'collection_id' : collection.collection_id}


@app.route('/delete_collection', methods=['POST'])
def delete_collection():
    """ Remove the specified collection from the user's library. """

    collection_id = request.form.get('collection_id') 
    user = crud.get_user_by_id(session['user_id'])
    collection = crud.get_collection_by_id(collection_id)
    collection_name = collection.name
    crud.remove_from_user_library(user, collection=collection)

    return f'{collection_name} has been removed from your library.'


#----------------------------------------------------------------------#
# *** Routes Related to User's Visualizations                          #
#----------------------------------------------------------------------#

@app.route('/pie')
def show_pie():
    """ Show a pie chart representing the genres enjoyed by a user. """

    # get data
    genre_data = crud.get_user_genre_data(session['user_id'])
    data = pd.Series(genre_data).reset_index(name='value').rename(columns={'index':'genre'})
    data['angle'] = data['value']/data['value'].sum() * 2 * pi
    data['color'] = Category20[len(genre_data)]
    source = ColumnDataSource(data=data)

    # build figure/plot
    p = figure(title="My Genre Pie", toolbar_location=None, tools="hover", # can also specify plot height
                tooltips=[("genre", "@genre"), ("count", "@value")], 
                x_range=(-0.5, 1.0))

    p.wedge(x=0, y=0, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color='white', legend_field='genre', 
            line_width=2, fill_color='color', source=source) 

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    # get displayable plot
    script, div = components(p)

    return render_template('vis_pie.html', plot_div=div, plot_script=script)


@app.route('/timeline')
def show_timeline():
    """ Show timeline plot illustrating a user's updates. """

    # get data
    log_data = crud.get_user_log(session['user_id'])
    data = {'title': [], 'media_type': [], 'rating': [], 'start_date': [], 'end_date':[]}
    for user_media_id in log_data:
        if log_data[user_media_id]['start_date']:
            data['title'].append(log_data[user_media_id]['title'])
            data['rating'].append(log_data[user_media_id]['rating'])
            start_date = datetime.combine(log_data[user_media_id]['start_date'],time.min)
            data['start_date'].append(start_date)
            if log_data[user_media_id]['start_date'] and (log_data[user_media_id]['end_date'] == None):
                data['end_date'].append(datetime.now())
            else:
                data['end_date'].append(datetime.combine(log_data[user_media_id]['end_date'],time.min))
            data['media_type'].append(log_data[user_media_id]['media_type'])
    colors = Category20[5] 
    cds_data = ColumnDataSource(data=data)

    movie_view = CDSView(source=cds_data,
            filters=[GroupFilter(column_name='media_type', group='movie')])
    book_view = CDSView(source=cds_data,
            filters=[GroupFilter(column_name='media_type', group='book')])
    tv_view = CDSView(source=cds_data,
            filters=[GroupFilter(column_name='media_type', group='tv')])

    # build figure/plot
    p = figure(y_range=(0, 5.5), x_range=(datetime(2010,1,1,0,0,0), datetime.now()), 
            plot_width=1000, plot_height=675, tools=["hover","box_zoom","wheel_zoom","pan"],
            tooltips=[("title", "@title"), ("media_type", "@media_type")], # TODO: add , ("date", x_val)
            title="timeline sorted by rating")
    p.hbar(y="rating", left='start_date', right='end_date', fill_alpha=0.5,
            height=0.35, view=book_view, fill_color=colors[0], source=cds_data) 
    p.diamond(y="rating", x='start_date', fill_alpha=0.5, size=35,
            view=movie_view, fill_color=colors[2], source=cds_data)
    p.hex(y="rating", x='start_date', fill_alpha=0.5, size=35,
            view=tv_view, fill_color=colors[4], source=cds_data)

    p.ygrid.grid_line_color = None
    p.xaxis.axis_label = "dates read"
    p.outline_line_color = None

    # get displayable plot
    script, div = components(p)

    return render_template('vis_timeline.html', plot_div=div, plot_script=script)



#----------------------------------------------------------------------#

# TODO: create media management functions: 

#       NTH: rename collection
#       NTH: remove items from collection
#       NTH: see/edit updates associated with this item.
#       NTH: bulk add items to collection
#       NTH: arrange items in collection 


#----------------------------------------------------------------------#

if __name__ == '__main__':
    connect_to_db(app, echo=False)
    app.run(debug=True, host='0.0.0.0')