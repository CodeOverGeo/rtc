"""SQLAlchemy models for RTC"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
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

    reviews = db.relationship('Review', backref='user',
                              cascade='all, delete-orphan')

    @classmethod
    def signup(cls, username, email, password, date_joined):
        """Sign up user

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

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


class Station(db.Model):
    """Station model for rtc app"""

    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)

    open_charge_id = db.Column(db.Integer, nullable=False)

    Title = db.Column(db.Text, nullable=False)

    AddressLine1 = db.Column(db.Text, nullable=False)

    Town = db.Column(db.Text, nullable=False)

    StateOrProvince = db.Column(db.Text, nullable=False)

    Postcode = db.Column(db.Integer, nullable=False)

    FormalName = db.Column(db.Text, nullable=False)

    type = db.Column(db.Text, nullable=False)

    in_operation = db.Column(db.Boolean, nullable=False)

    reviews = db.relationship('Review', backref='stations')

    def serialize(self):
        """Serialize Station instance to a dict"""
        return {
            'id': self.id,
            'open_charge_id': self.open_charge_id,
            'location': self.location,
            'type': self.type,
            'in_operation': self.in_operation,
        }


class Review(db.Model):
    """Reviews model for rtc app"""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    score = db.Column(db.Integer, nullable=False)

    post = db.Column(db.Text, nullable=False)

    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)

    updated_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    station_id = db.Column(db.Integer, db.ForeignKey(
        'stations.id'), nullable=False)

    @property
    def readable_created_date(self):
        """Returns a user readable date"""

        return self.created_at.strftime('%a %b %d %Y, %I:%M %p')

    @property
    def readable_updated_date(self):
        """Returns a user readable date"""

        return self.updated_date.strftime('%a %b %d %Y, %I:%M %p')


# class Tag(db.Model):
#     """Tag model for rtc app"""

#     __tablename__ = 'tags'

#     id = db.Column(db.Integer, primary_key=True)

#     tags = db.Column(db.String, nullable=False)


# class Station_Tag(db.Model):
#     """Station to Tag joining model"""

#     __tablename__ = 'station_tags'

#     id = db.Column(db.Integer, primary_key=True)

#     station_id = db.Column(db.Integer, db.ForeignKey(
#         'stations.id'), nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def connect_db(app):
    db.app = app
    db.init_app(app)
