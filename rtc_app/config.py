import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Charger')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql:///rtc')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    DEBUG_TB_INTERCEPT_REDIRECTS = False
