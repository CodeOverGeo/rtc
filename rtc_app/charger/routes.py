from flask import render_template, flash, redirect, session, url_for, g, Blueprint
from rtc_app.models import Review, Station, User, db
from rtc_app.api.routes import get_stations
from rtc_app.charger.forms import ReviewForm
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
        form = ReviewForm()

        station = get_stations(charger_id)
        return render_template('charge/station.html', station=station, form=form)


@charger.route('/station/<int:charger_id>/reviews/add', methods=['POST'])
def add_comment(charger_id):
    """Add a review for a specific charging station

    If valid, update review and redirect to station page"""

    if not g.user:
        flash('Access unauthorized.', 'danger')
        return redirect('/')

    form = ReviewForm()

    import pdb
    pdb.set_trace()

    if form.validate_on_submit():
        print('**********************inside')
        review = Review(score=form.score.data,
                        post=form.post.data,
                        user_id=g.user.id,
                        station_id=charger_id)
        db.session.add(review)
        db.session.commit()

        return redirect(f'station/{review.station.open_charge_id}')

    return redirect('/search')


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
