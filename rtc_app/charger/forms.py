from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Email, Length


class StationForm(FlaskForm):
    """Form for searching for stations."""

    address = StringField('Address', validators=[DataRequired()])


class ReviewForm(FlaskForm):
    """Form for adding review for station"""

    score = HiddenField('rating', validators=[InputRequired()])
    post = StringField('Comment', validators=[DataRequired()])
