"""RTC Front End App"""

from flask.config import Config
from flask import Flask

from rtc_app.main.routes import main
from rtc_app.charger.routes import charger
from rtc_app.users.routes import users
from rtc_app.api.routes import api_bp


from rtc_app.config import Config


from rtc_app.models import db, connect_db, User

CURR_USER_KEY = 'curr_user'


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    app.register_blueprint(users)
    app.register_blueprint(charger)
    app.register_blueprint(main)
    app.register_blueprint(api_bp)

    connect_db(app)
    # db.drop_all()
    db.create_all()

    return app
