"""RTC Front End App"""

from flask import Flask, request, render_template, flash, redirect, make_response, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Station, Review, Tag, Station_Tag

import requests

from api import api_bp

import os


CURR_USER_KEY = 'curr_user'
OPEN_MAP_API_KEY = 'e480c0a2-c3be-438b-90ea-db01e1d26c74'
BASE_URL_OPEN_MAPS = 'https://api.openchargemap.io/v3/poi/'

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(api_bp, url_prefix='/api')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///rtc')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Charger')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
db.create_all()


##################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup

    Create new user and add to DB. Redirect to home page.

    If form is not valid, present form.

    If username is taken: flash message and re-present form.
    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                date_joined=User.date_joined.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash('Username already taken', 'danger')
            return redirect('users/signup.html', form=form)

        do_login(user)

        return redirect('/search')

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Welcome, {user.username}!", 'success')
            return redirect('/search')

        else:
            flash('Username or password incorrect.', 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle user logout"""

    do_logout()

    flash('Logout successful!', 'success')
    return redirect('/login')

########################################################
# Charger routes


@app.route('/search')
def search():
    """Render main search page for chargers"""

    if not g.user:
        flash('Access unauthorized!', 'danger')
        return redirect('/')

    return render_template('charge/search.html')


@app.route('/station/<int:charger_id>')
def charger(charger_id):
    """Render charger detail page"""

    if not g.user:
        flash('Access unauthorized.', 'danger')
        return redirect('/')
    try:
        resp = requests.get(f'http://localhost:5000/api/stations/{charger_id}')

        if resp.status_code == 200:
            response = resp.json()  # resp.data()
            render_template('charge/station.html', station=response)
        elif resp.status_code == 204:

            payload = {'output': 'json', 'chargepointid': charger_id,
                       'key': OPEN_MAP_API_KEY}
            resp = requests.get(
                'https://api.openchargemap.io/v3/poi/', params=payload)
            # resp.json(), resp.data()
            # import pdb
            # pdb.set_trace()
            return('WORKED')
        else:
            return 'KINDA FAILED'

    finally:
        return 'FAILED'


@app.route('/')
def homepage():
    """Root route redirects to Homepage"""

    return render_template('home.html')


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
