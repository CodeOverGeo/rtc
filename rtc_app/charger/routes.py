from flask import render_template, flash, redirect, session, url_for, g, Blueprint
from rtc_app.models import Station, User
from rtc_app.api.routes import get_stations
import requests

charger = Blueprint('charger', __name__)
CURR_USER_KEY = 'curr_user'


########################################################
# Charger routes


@charger.route('/search')
def search():
    """Render main search page for chargers"""

    if not g.user:
        flash('Access unauthorized!', 'danger')
        return redirect('/')

    return render_template('charge/search.html')


@charger.route('/station/<int:charger_id>')
def stations(charger_id):
    """Render charger detail page"""

    if not g.user:
        flash('Access unauthorized.', 'danger')
        return redirect('/')
    else:
        station = get_stations(charger_id)
        return render_template('charge/station.html', station=station)

        # resp.json(), resp.data()
        # import pdb
        # pdb.set_trace()
        return('WORKED')


@ charger.before_request
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

@ charger.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
