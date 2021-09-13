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
    pass


class Tags(db.Model):
    pass


class Station_Tags(db.Model):
    pass
