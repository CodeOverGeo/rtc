from flask import render_template, flash, redirect, session, g, Blueprint
from rtc_app.models import User
import requests

charger = Blueprint('charger', __name__)
CURR_USER_KEY = 'curr_user'
OPEN_MAP_API_KEY = 'e480c0a2-c3be-438b-90ea-db01e1d26c74'

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


@charger.before_request
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

@charger.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
