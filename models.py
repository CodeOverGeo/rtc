"""SQLAlchemy models for RTC"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

brcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model for rtc app"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, nullable=False, unique=True)

    date_joined = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())

    @classmethod
    def signup(cls, username, email, password, date_joined):
        """Sign up user

        Hashes password and adds user to system.
        """

        hashed_pwd = brcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            date_joined=date_joined,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates user using username and hashed password

        This user in found, return user object.
        If username is not found or password is incorrect, return False
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Stations(db.Model):
    """Station model for rtc app"""

    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)

    location = db.Column(db.Text, nullable=False)

    type = db.Column(db.Text, nullable=False)

    in_operation = db.Column(db.Boolean, nullable=False)


class Reviews(db.Model):
    """Reviews model for rtc app"""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    score = db.Column(db.Integer, nullable=False)

    post = db.Column(db.Text, nullable=False)

    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)

    updated_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def readable_date(self):
        """Returns a user readable date"""

        return self.created_at.strftime('%a %b %d %Y, %I:%M %p')

    @property
    def readable_date(self):
        """Returns a user readable date"""

        return self.updated_date.strftime('%a %b %d %Y, %I:%M %p')


class Tags(db.Model):
    """Tag model for rtc app"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    tags = db.Column(db.String, nullable=False)


class Station_Tags(db.Model):
    """Station to Tag joining model"""

    __tablename__ = 'station_tags'

    id = db.Column(db.Integer, primary_key=True)

    station_id = db.Column(db.Integer, db.ForeignKey(
        'stations.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def connect_db(app):
    db.app = app
    db.init_app(app)
