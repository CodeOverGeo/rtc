"""Flask app for RTC API"""

from flask import request, jsonify, make_response, Blueprint


from models import db, connect_db, User, Station, Review, Tag, Station_Tag

api_bp = Blueprint('api', __name__)


#####################################
# Station api routes


@api_bp.route('/home')
def home():
    return "Hello from API route"


@api_bp.route('/stations/<int:station_id>')
def get_stations(station_id):
    """REturn data on a specific charging station

    Returns data in JSON
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
        return jsonify(station=station.serialize())

    return '', 204
