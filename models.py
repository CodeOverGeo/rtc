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
                             default=datetime.datetime.utcnow)

    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
