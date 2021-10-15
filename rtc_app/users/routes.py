
from flask import render_template, flash, redirect, session, g, Blueprint

from sqlalchemy.exc import IntegrityError

from rtc_app.users.forms import UserAddForm, LoginForm
from rtc_app.models import db, connect_db, User

from rtc_app.users.utils import do_login, do_logout

users = Blueprint('users', __name__)

CURR_USER_KEY = 'curr_user'


@users.route('/signup', methods=['GET', 'POST'])
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


@users.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if not g.user:
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

    else:
        return redirect('/search')


@users.route('/logout')
def logout():
    """Handle user logout"""

    do_logout()

    flash('Logout successful!', 'success')
    return redirect('/login')


@users.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@users.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
