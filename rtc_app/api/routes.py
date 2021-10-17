"""Flask app for RTC API"""

from flask import jsonify, make_response, Blueprint
import requests


from rtc_app.models import db, connect_db, User, Station, Review

api_bp = Blueprint('api_bp', __name__)
CURR_USER_KEY = 'curr_user'
BASE_URL_OPEN_MAPS = 'https://api.openchargemap.io/v3/poi/'
OPEN_MAP_API_KEY = 'e480c0a2-c3be-438b-90ea-db01e1d26c74'

#####################################
# Station api routes


# @api_bp.route('/api/stations/<int:station_id>')
def get_stations(station_id):
    """Return data on a specific charging station
    """

    # charger = Station(
    #     open_charge_id=1,
    #     location='home',
    #     type="charger",
    #     in_operation=True,
    # )

    # db.session.add(charger)
    # db.session.commit()

    exists = db.session.query(Station.id).filter_by(
        open_charge_id=station_id).first() is not None
    if exists:
        station = Station.query.filter_by(
            open_charge_id=station_id).first_or_404()
        return station

    else:
        query = {'key': OPEN_MAP_API_KEY, 'chargepointid': station_id}
        station = requests.get(BASE_URL_OPEN_MAPS, query)
        response = station.json()
        print('********************')
        print(response)
    return False


def post_station():
    pass
