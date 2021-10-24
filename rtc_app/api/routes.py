"""Flask app for RTC API"""

from pdb import set_trace
from flask import jsonify, make_response, Blueprint
import requests
from requests.exceptions import HTTPError


from rtc_app.models import db, User, Station, Review

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
        try:
            print('*************inside')
            query = {'key': OPEN_MAP_API_KEY, 'chargepointid': station_id}
            response = requests.get(BASE_URL_OPEN_MAPS, query)
            response.raise_for_status
            data = response.json()
            return post_station(data)
        except HTTPError as http_err:
            return (f'HTTP error occurred: {http_err}')
        except Exception as err:
            return (f'Other error occurred: {err}')


def post_station(data):
    """Post new station onto database"""
    print('*******************posting new station')
    station = data[0]

    new_station = Station(
        open_charge_id=station['ID'],
        Title=station['AddressInfo']['Title'],
        AddressLine1=station['AddressInfo']['AddressLine1'],
        Town=station['AddressInfo']['Town'],
        StateOrProvince=station['AddressInfo']['StateOrProvince'],
        Postcode=station['AddressInfo']['Postcode'],
        FormalName=station['Connections'][0]['ConnectionType']['FormalName'] or 'Unknown',
        type=station['Connections'][0]['ConnectionType']['Title'] or 'Unknown',)

    db.session.add(new_station)
    db.session.commit()

    print('**********************set trace')
    return new_station
