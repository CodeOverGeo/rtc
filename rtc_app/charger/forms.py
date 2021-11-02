from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange
from wtforms.widgets.core import HiddenInput


class StationForm(FlaskForm):
    """Form for searching for stations."""

    address = StringField('Address', validators=[DataRequired()])


class ReviewForm(FlaskForm):
    """Form for adding review for station"""

    score = HiddenField('rating', default=5,
                        validators=[InputRequired()])
    post = StringField('Comment', validators=[InputRequired()])
