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

    # print('\n\n DEBUGGING ... session:',session,'\n****\n') ###

    return render_template('homepage.html')


# browse all media route (by genre, media type, etc.)
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
def show_log_in_page():
    """ Show the log-in page for an existing user. """

    return render_template('log_in.html')


@app.route('/verify_login', methods=['POST'])
def verify_login():
    """ Verify a user's login information. """

    email = request.form.get('email')
    pwd = request.form.get('pwd')

    user = crud.get_user_by_email(email)

    # TODO: currently if someone is logged in already, this allows someone else to log in and overwrite the session. fix that!
    if user and user.pwd == pwd:
        flash(f'Welcome back, {user.fname}! You are now logged in.')
        session['user_id'] = user.user_id
        # print(f"\n\n DEBUGGING ... YOU LOGGED IN WITH USER ID # {session['user_id']}") ###
    else:
        flash(f'User email and/or password is incorrect. Please try again.')

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


@app.route('/user_homepage') # make this user-specific...
def show_user_homepage():
    """ Show a logged-in user their personal homepage. """

    # TODO: write me!
    user = crud.get_user_by_id(session['user_id'])

    return render_template('user_homepage.html', user=user)


# add media item (check if in db first, then make get request to appropriate API)
@app.route('/search')
def search_for_media_item():
    """ Show search page. """

    return render_template('searchpage.html')


@app.route('/process_search')
def process_search():
    """ Search database for the specified media item.
        If not in the database, redirect to /add_media route. """



@app.route('/add_media')
def add_media_item():
    """ Make GET request to the appropriate API.
        Add item to the database. """



#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')